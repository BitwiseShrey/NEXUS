"""
NEXUS Disruption Impact Analysis Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.api_schemas import ImpactAnalyzeRequest, ImpactAnalyzeResponse
from impact.impact_engine import ImpactEngine

router = APIRouter(tags=["Impact Analysis"])


@router.post("/impact/analyze", response_model=ImpactAnalyzeResponse, summary="Analyze Disruption Propagation")
def analyze_disruption_impact(req: ImpactAnalyzeRequest, db: Session = Depends(get_db)):
    """
    Simulates graph-based propagation when a facility or corridor fails,
    quantifying downstream dependent products, exposed warehouses, shortage units,
    and projected service-level drop.
    """
    engine = ImpactEngine(db=db)

    if req.entity_type.upper() == "SUPPLIER":
        result = engine.analyze_supplier_disruption(
            supplier_id=req.entity_id,
            capacity_reduction=req.capacity_reduction,
            duration_days=req.duration_days
        )
    elif req.entity_type.upper() == "WAREHOUSE":
        result = engine.analyze_warehouse_disruption(
            warehouse_id=req.entity_id,
            duration_days=req.duration_days
        )
    elif req.entity_type.upper() == "ROUTE":
        result = engine.analyze_route_disruption(
            route_id=req.entity_id,
            duration_days=req.duration_days
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported entity type: {req.entity_type}")

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
