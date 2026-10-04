"""
Unit Tests for NEXUS Scenario Simulation Engine
"""

from simulation.scenario_engine import ScenarioEngine, ScenarioType


def test_scenario_isolation_and_supplier_failure():
    engine = ScenarioEngine()
    initial_cap = engine.base_state.suppliers["SUP_001"]["capacity"]

    # Run 80% reduction
    res = engine.run_scenario(
        ScenarioType.SUPPLIER_FAILURE,
        {"supplier_id": "SUP_001", "capacity_reduction": 0.80, "duration_days": 10}
    )

    sim_state = res["state_object"]
    simulated_cap = sim_state.suppliers["SUP_001"]["capacity"]

    # Verify simulated reduction
    assert round(simulated_cap, 1) == round(initial_cap * 0.20, 1)

    # Verify base state was not mutated (non-destructive)
    assert engine.base_state.suppliers["SUP_001"]["capacity"] == initial_cap


def test_scenario_demand_spike():
    engine = ScenarioEngine()
    total_base_demand = sum([dz["demand"] for dz in engine.base_state.demand_zones.values()])

    res = engine.run_scenario(
        ScenarioType.DEMAND_SPIKE,
        {"demand_spike_percent": 0.50}
    )

    sim_demand = res["simulated_network_state"]["total_demand_units"]
    assert sim_demand > total_base_demand


def test_scenario_warehouse_shutdown():
    engine = ScenarioEngine()
    res = engine.run_scenario(
        ScenarioType.WAREHOUSE_SHUTDOWN,
        {"warehouse_id": "WH_01"}
    )
    sim_state = res["state_object"]
    assert sim_state.warehouses["WH_01"]["status"] == "SHUTDOWN"
    # Inbound and outbound routes should be blocked
    wh_routes = [r for r in sim_state.routes.values() if r["origin"] == "WH_01" or r["destination"] == "WH_01"]
    assert all(r["status"] == "BLOCKED" for r in wh_routes)
