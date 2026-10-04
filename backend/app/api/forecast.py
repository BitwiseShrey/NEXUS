"""
NEXUS Demand Forecasting Endpoints
"""

from datetime import datetime
from pathlib import Path
import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models import Forecast
from backend.app.schemas.api_schemas import ForecastRequest, ForecastResponse
from ml.forecasting.xgboost_forecaster import DemandForecaster

router = APIRouter(tags=["Demand Forecasting"])


@router.post("/forecast", response_model=ForecastResponse, summary="Generate Demand Forecast")
def generate_demand_forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    """
    Generates multi-horizon demand forecasts using the validated XGBoost regressor,
    benchmarked against Naive and Moving Average baselines.
    """
    forecaster = DemandForecaster(random_seed=settings.RANDOM_SEED)
    try:
        forecaster.load_model(settings.MODEL_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting model not ready: {str(e)}")

    # Load recent series
    meta_path = Path(settings.MODEL_DIR) / "forecasting_metadata.json"
    benchmarks = {}
    if meta_path.exists():
        with open(meta_path) as f:
            benchmarks = json.load(f).get("metrics", {})

    # Create recent demand sequence for recursive forecast
    demand_parquet = Path(settings.DATA_PROCESSED_DIR) / "walmart_demand_cleaned.parquet"
    if demand_parquet.exists():
        df_dem = pd.read_parquet(demand_parquet)
        recent_history = (
            df_dem[df_dem["Store"] == 1]
            .groupby("Date")["Weekly_Sales"]
            .sum()
            .reset_index()
            .rename(columns={"Date": "date", "Weekly_Sales": "demand"})
            .tail(24)
        )
    else:
        # Fallback synthetic sequence
        recent_history = pd.DataFrame({
            "date": pd.date_range(end=datetime.utcnow(), periods=16, freq="W"),
            "demand": [25000 + i * 200 for i in range(16)]
        })

    forecasts = forecaster.forecast_future(recent_history, horizon_steps=req.horizon_weeks)

    # Persist forecast to DB
    fc_id = f"FC_{uuid.uuid4().hex[:8].upper()}"
    fc_record = Forecast(
        forecast_id=fc_id,
        product_id=req.product_id,
        model_name=forecaster.best_model_name or "XGBoost_Regressor",
        horizon_days=req.horizon_weeks * 7,
        forecast_values={"values": forecasts},
        metrics=benchmarks
    )
    db.add(fc_record)
    db.commit()

    return {
        "product_id": req.product_id,
        "model_name": forecaster.best_model_name or "XGBoost_Regressor",
        "horizon_weeks": req.horizon_weeks,
        "forecasted_demand": forecasts,
        "metrics_benchmarks": benchmarks,
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/forecasts", summary="List historical forecast runs")
def list_forecasts(db: Session = Depends(get_db)):
    fcs = db.query(Forecast).order_by(Forecast.generated_at.desc()).limit(20).all()
    return [{
        "forecast_id": f.forecast_id,
        "product_id": f.product_id,
        "model_name": f.model_name,
        "horizon_days": f.horizon_days,
        "forecast_values": f.forecast_values,
        "metrics": f.metrics,
        "generated_at": f.generated_at.isoformat() if f.generated_at else None
    } for f in fcs]
