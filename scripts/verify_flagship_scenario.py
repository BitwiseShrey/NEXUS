import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.database import SessionLocal
from simulation.scenario_engine import ScenarioEngine, ScenarioType
from optimization.ortools_optimizer import SupplyChainOptimizer

db = SessionLocal()
try:
    scenario_engine = ScenarioEngine(db)
    sim_res = scenario_engine.run_scenario(
        ScenarioType.SUPPLIER_FAILURE,
        {"supplier_id": "SUP_001", "capacity_reduction": 0.80, "duration_days": 10}
    )
    sim_state = sim_res["state_object"]
    print("Simulated state created.")
    print("Demand:", sim_res["simulated_network_state"]["total_demand_units"])
    print("Capacity balance:", sim_res["simulated_network_state"]["net_capacity_balance"])

    optimizer = SupplyChainOptimizer(risk_aversion_weight=50.0, shortage_penalty_unit=350.0)
    comparison = optimizer.compare_with_baseline(sim_state)

    print("\n--- BASELINE RESULTS ---")
    print("Total Cost:", f"INR {comparison['baseline']['total_cost']:,.2f}")
    print("Procurement Cost:", f"INR {comparison['baseline']['procurement_cost']:,.2f}")
    print("Transport Cost:", f"INR {comparison['baseline']['transport_cost']:,.2f}")
    print("Holding Cost:", f"INR {comparison['baseline']['holding_cost']:,.2f}")
    print("Shortage Penalty:", f"INR {comparison['baseline']['shortage_cost']:,.2f}")
    print("Unmet Shortage Units:", f"{comparison['baseline']['total_shortage_units']:,.2f}")
    print("Service Level:", f"{comparison['baseline']['service_level'] * 100:.2f}%")

    print("\n--- NEXUS OPTIMIZED RESULTS ---")
    print("Total Cost:", f"INR {comparison['nexus_optimized']['total_cost']:,.2f}")
    print("Procurement Cost:", f"INR {comparison['nexus_optimized']['procurement_cost']:,.2f}")
    print("Transport Cost:", f"INR {comparison['nexus_optimized']['transport_cost']:,.2f}")
    print("Holding Cost:", f"INR {comparison['nexus_optimized']['holding_cost']:,.2f}")
    print("Shortage Penalty:", f"INR {comparison['nexus_optimized']['shortage_cost']:,.2f}")
    print("Unmet Shortage Units:", f"{comparison['nexus_optimized']['total_shortage_units']:,.2f}")
    print("Service Level:", f"{comparison['nexus_optimized']['service_level'] * 100:.2f}%")
    print("Solver Execution Time:", f"{comparison['nexus_optimized']['execution_time_seconds']:.4f}s")
    print("Solver Status:", comparison['nexus_optimized']['status'])

    comp = comparison["impact_comparison"]
    print("\n--- COMPARISON / IMPACT ---")
    print("Cost Saved INR:", f"INR {comp['cost_saved_inr']:,.2f}")
    print("Cost Reduction %:", f"{comp['cost_reduction_percent']}%")
    print("Shortage Reduction Units:", f"{comp['shortage_reduction_units']:,.2f}")
    print("Service Level Improvement pp:", f"+{comp['service_level_improvement_percentage_points']}%")

finally:
    db.close()
