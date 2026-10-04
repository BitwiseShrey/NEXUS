"""
Unit Tests for NEXUS Optimization Engine (Google OR-Tools) and Baseline Comparison
"""

from simulation.scenario_engine import ScenarioEngine, ScenarioType
from optimization.ortools_optimizer import SupplyChainOptimizer
from optimization.baseline_optimizer import BaselineOptimizer


def test_ortools_optimizer_feasibility():
    engine = ScenarioEngine()
    sim_res = engine.run_scenario(
        ScenarioType.SUPPLIER_FAILURE,
        {"supplier_id": "SUP_001", "capacity_reduction": 0.80, "duration_days": 10}
    )
    sim_state = sim_res["state_object"]

    optimizer = SupplyChainOptimizer(risk_aversion_weight=50.0)
    opt_res = optimizer.solve(sim_state)

    assert opt_res["status"] == "OPTIMAL"
    assert opt_res["total_cost"] > 0
    assert 0.0 <= opt_res["service_level"] <= 1.0
    assert opt_res["allocations_count"] > 0


def test_baseline_vs_nexus_comparison():
    engine = ScenarioEngine()
    sim_res = engine.run_scenario(
        ScenarioType.COMBINED_DISRUPTION,
        {"supplier_id": "SUP_001", "capacity_reduction": 0.85, "route_id": "RT_0001"}
    )
    sim_state = sim_res["state_object"]

    optimizer = SupplyChainOptimizer()
    comparison = optimizer.compare_with_baseline(sim_state)

    assert "baseline" in comparison
    assert "nexus_optimized" in comparison
    assert "impact_comparison" in comparison

    comp = comparison["impact_comparison"]
    # NEXUS multi-echelon rebalancing should avoid rigid bottleneck shortages
    assert comp["is_nexus_superior"] is True
    assert comp["service_level_improvement_percentage_points"] >= 0.0
