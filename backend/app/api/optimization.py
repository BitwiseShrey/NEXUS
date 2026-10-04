"""
NEXUS Optimization and Decision Engine Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import OptimizationRun
from backend.app.schemas.api_schemas import OptimizeRequest, OptimizeResponse
from impact.impact_engine import ImpactEngine
from optimization.ortools_optimizer import SupplyChainOptimizer
from recommendation.recommendation_engine import RecommendationEngine
from simulation.scenario_engine import ScenarioEngine, ScenarioType

router = APIRouter(tags=["Optimization & Decision Intelligence"])


@router.post("/optimize", response_model=OptimizeResponse, summary="Run OR-Tools Optimization with Baseline Comparison")
def run_supply_chain_optimization(req: OptimizeRequest, db: Session = Depends(get_db)):
    """
    Simulates the requested disruption scenario, solves optimal multi-echelon network allocation
    using Google OR-Tools, generates an empirical comparison against baseline heuristic response,
    and produces an explainable recommendation.
    """
    try:
        sc_type = ScenarioType(req.scenario_type.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid scenario_type '{req.scenario_type}'")

    # 1. Simulate Scenario Shock
    scenario_engine = ScenarioEngine(db)
    sim_res = scenario_engine.run_scenario(sc_type, req.parameters)
    sim_state = sim_res["state_object"]

    # 2. Run Impact Propagation
    impact_engine = ImpactEngine(db=db)
    target_sup = req.parameters.get("supplier_id", "SUP_001")
    impact_res = impact_engine.analyze_supplier_disruption(
        supplier_id=target_sup,
        capacity_reduction=float(req.parameters.get("capacity_reduction", 0.80)),
        duration_days=int(req.parameters.get("duration_days", 10))
    )

    # 3. Solve OR-Tools Optimization and Baseline Benchmark
    optimizer = SupplyChainOptimizer(risk_aversion_weight=req.risk_aversion_weight)
    comparison = optimizer.compare_with_baseline(sim_state)

    # 4. Generate Explainable Recommendation
    rec_engine = RecommendationEngine(db)
    recommendation = rec_engine.generate_recommendation(
        scenario_name=f"{req.scenario_type} [{target_sup}]",
        impact_result=impact_res,
        comparison_result=comparison,
        persist=True
    )

    return {
        "baseline": comparison["baseline"],
        "nexus_optimized": comparison["nexus_optimized"],
        "impact_comparison": comparison["impact_comparison"],
        "recommendation": recommendation
    }


@router.get("/optimization-runs", summary="List historical optimization runs")
def list_optimization_runs(db: Session = Depends(get_db)):
    runs = db.query(OptimizationRun).order_by(OptimizationRun.created_at.desc()).limit(20).all()
    return [{
        "run_id": r.run_id,
        "scenario_name": r.scenario_name,
        "objective_type": r.objective_type,
        "status": r.status,
        "total_cost": r.total_cost,
        "service_level": r.service_level,
        "shortages_total": r.shortages_total,
        "procurement_cost": r.procurement_cost,
        "transportation_cost": r.transportation_cost,
        "penalty_cost": r.penalty_cost,
        "runtime_seconds": r.runtime_seconds,
        "created_at": r.created_at.isoformat() if r.created_at else None
    } for r in runs]
