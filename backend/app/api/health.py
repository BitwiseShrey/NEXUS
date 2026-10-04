"""
NEXUS Health and Diagnostics Endpoint
"""

from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.config import settings
from backend.app.database import get_db

router = APIRouter(tags=["System Health"])


@router.get("/health", summary="System Health & Readiness Check")
def check_health(db: Session = Depends(get_db)):
    """
    Validates backend API health, relational database connection, and serialized ML model artifact readiness.
    """
    # Test DB
    db_status = "HEALTHY"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    # Check Model Artifacts
    model_dir = Path(settings.MODEL_DIR)
    models_ready = {
        "demand_forecaster": (model_dir / "demand_forecaster.joblib").exists(),
        "supplier_risk_model": (model_dir / "supplier_risk_model.joblib").exists(),
        "anomaly_detector": (model_dir / "anomaly_model.joblib").exists()
    }

    return {
        "status": "ONLINE",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": db_status,
        "models_loaded": models_ready,
        "all_systems_operational": db_status == "HEALTHY" and all(models_ready.values())
    }
