"""
NEXUS Risk Prediction Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.schemas.api_schemas import (
    RiskPredictRequest, RiskPredictResponse
)
from digital_twin.risk_engine import UnifiedRiskEngine
from ml.risk.supplier_risk_model import SupplierRiskModel

router = APIRouter(tags=["Risk Engine & Prediction"])


@router.post("/risk/predict", response_model=RiskPredictResponse, summary="Predict Supplier Disruption Risk")
def predict_supplier_risk(req: RiskPredictRequest):
    """
    Evaluates supplier operational indicators through trained supervised ML model,
    returning disruption probability, risk tier, and key risk drivers.
    """
    risk_model = SupplierRiskModel(random_seed=settings.RANDOM_SEED)
    try:
        risk_model.load_model(settings.MODEL_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk model not available: {str(e)}")

    features = req.model_dump()
    result = risk_model.predict_risk(features)
    return result


@router.get("/risks", summary="Unified Network-Wide Risk Assessment")
def get_network_risk_profile(db: Session = Depends(get_db)):
    """
    Returns explainable multi-dimensional risk scores:
    Supplier Risk, Inventory Stockout Risk, Route Transit Risk, and Warehouse Congestion.
    """
    engine = UnifiedRiskEngine(db)
    return engine.compute_network_risk_profile()
