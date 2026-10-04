"""
NEXUS Recommendation Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Recommendation

router = APIRouter(tags=["Recommendations"])


@router.get("/recommendations", summary="List generated actionable recommendations")
def list_recommendations(db: Session = Depends(get_db)):
    """
    Returns AI-generated actionable recommendations created from optimization solutions.
    """
    recs = db.query(Recommendation).order_by(Recommendation.created_at.desc()).limit(20).all()
    return [{
        "recommendation_id": r.recommendation_id,
        "run_id": r.run_id,
        "title": r.title,
        "reason": r.reason,
        "affected_entities": r.affected_entities,
        "action_type": r.action_type,
        "expected_benefit": r.expected_benefit,
        "expected_cost": r.expected_cost,
        "confidence_score": r.confidence_score,
        "created_at": r.created_at.isoformat() if r.created_at else None
    } for r in recs]
