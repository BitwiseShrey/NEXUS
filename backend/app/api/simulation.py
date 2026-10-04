"""
NEXUS Scenario Simulation Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.api_schemas import (
    ScenarioSimulateRequest, ScenarioSimulateResponse
)
from simulation.scenario_engine import ScenarioEngine, ScenarioType

router = APIRouter(tags=["Scenario Simulation"])


@router.post("/scenario/simulate", response_model=ScenarioSimulateResponse, summary="Simulate Disruption Scenario")
def simulate_scenario(req: ScenarioSimulateRequest, db: Session = Depends(get_db)):
    """
    Simulates operational shocks on an in-memory clone of the digital twin
    without permanently altering the base persistent state.
    """
    try:
        sc_type = ScenarioType(req.scenario_type.upper())
    except ValueError:
        valid_types = [t.value for t in ScenarioType]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario_type '{req.scenario_type}'. Must be one of: {valid_types}"
        )

    engine = ScenarioEngine(db)
    result = engine.run_scenario(sc_type, req.parameters)

    # Exclude internal state_object from JSON serialization
    return {
        "scenario_type": result["scenario_type"],
        "parameters": result["parameters"],
        "applied_disruptions": result["applied_disruptions"],
        "simulated_network_state": result["simulated_network_state"]
    }
