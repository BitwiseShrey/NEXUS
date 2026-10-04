"""
NEXUS Anomaly Detection Endpoints
"""

from fastapi import APIRouter, HTTPException
import pandas as pd

from backend.app.config import settings
from backend.app.schemas.api_schemas import AnomalyDetectRequest, AnomalyDetectResponse
from ml.anomaly.isolation_forest_detector import AnomalyDetector

router = APIRouter(tags=["Anomaly Detection"])


@router.post("/anomaly/detect", response_model=AnomalyDetectResponse, summary="Detect Operational Anomalies")
def detect_anomalies(req: AnomalyDetectRequest):
    """
    Scans submitted supply-chain events using Isolation Forest to detect demand spikes,
    unusual delivery delays, and order pattern anomalies.
    """
    detector = AnomalyDetector()
    try:
        detector.load_model(settings.MODEL_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detector not loaded: {str(e)}")

    df_events = pd.DataFrame(req.events)
    if df_events.empty:
        return {"total_events_scanned": 0, "anomalies_detected_count": 0, "anomalies": []}

    anomalies = detector.detect_anomalies(df_events)
    return {
        "total_events_scanned": len(df_events),
        "anomalies_detected_count": len(anomalies),
        "anomalies": anomalies
    }
