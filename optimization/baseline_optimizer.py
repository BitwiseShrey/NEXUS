"""
NEXUS Baseline Supply Chain Response
Simulates standard un-optimized heuristic response during disruptions:
- Rigid primary supplier assignments (no agile substitution)
- Static routing (no detour around blocked corridors)
- High stockouts and penalty costs
"""

from typing import Dict, Any, List
import numpy as np
from simulation.scenario_engine import SimulationState


class BaselineOptimizer:
    """
    Computes business outcomes under naive, static supply chain operations without NEXUS intelligence.
    """

    @staticmethod
    def solve(
        sim_state: SimulationState,
        shortage_penalty_per_unit: float = 350.0,
        holding_cost_per_unit: float = 12.0
    ) -> Dict[str, Any]:
        """
        Executes static allocation: each demand zone attempts to fulfill only from its primary local source.
        Disrupted suppliers do not get substituted dynamically.
        """
        total_demand = sum([dz["demand"] for dz in sim_state.demand_zones.values()])

        procurement_cost = 0.0
        transportation_cost = 0.0
        total_shortage = 0.0
        total_fulfilled = 0.0
        risk_exposure = 0.0

        # In baseline operations, demand zones draw from warehouses. If upstream suppliers fail,
        # warehouses can only supply what is available without dynamic reallocation.
        active_supplier_caps = {
            s_id: s["capacity"] if s["status"] != "DISRUPTED" else s["capacity"]
            for s_id, s in sim_state.suppliers.items()
        }

        # Check blocked routes
        blocked_routes = {
            (r["origin"], r["destination"]) for r in sim_state.routes.values() if r["status"] == "BLOCKED"
        }

        for dz_id, dz in sim_state.demand_zones.items():
            req_demand = dz["demand"]
            # Baseline attempts to draw from primary warehouse
            wh_id = f"WH_{(hash(dz_id) % 10) + 1:02d}"

            # Check if corridor is severed
            if (wh_id, dz_id) in blocked_routes:
                total_shortage += req_demand
                continue

            wh = sim_state.warehouses.get(wh_id, {})
            if wh.get("status") == "SHUTDOWN":
                total_shortage += req_demand
                continue

            # Check upstream primary supplier for this commodity
            sup_id = f"SUP_{(hash(wh_id) % 20) + 1:03d}"
            sup = sim_state.suppliers.get(sup_id, {})
            avail_cap = active_supplier_caps.get(sup_id, 0.0)

            fulfilled = min(req_demand, avail_cap)
            shortage = req_demand - fulfilled

            active_supplier_caps[sup_id] = max(0.0, avail_cap - fulfilled)

            total_fulfilled += fulfilled
            total_shortage += shortage

            unit_cost = sup.get("unit_cost", 150.0)
            procurement_cost += fulfilled * unit_cost
            transportation_cost += fulfilled * 25.0  # nominal average freight
            risk_exposure += (fulfilled / max(total_demand, 1.0)) * sup.get("risk_score", 0.1)

        penalty_cost = total_shortage * shortage_penalty_per_unit
        holding_cost = total_fulfilled * holding_cost_per_unit
        total_cost = procurement_cost + transportation_cost + holding_cost + penalty_cost
        service_level = round(float(total_fulfilled / max(total_demand, 1.0)), 4)

        return {
            "mode": "BASELINE_UNOPTIMIZED",
            "status": "COMPLETED",
            "total_demand": round(total_demand, 1),
            "total_fulfilled": round(total_fulfilled, 1),
            "total_shortages": round(total_shortage, 1),
            "service_level": service_level,
            "procurement_cost": round(procurement_cost, 2),
            "transportation_cost": round(transportation_cost, 2),
            "penalty_cost": round(penalty_cost, 2),
            "holding_cost": round(holding_cost, 2),
            "total_cost": round(total_cost, 2),
            "risk_exposure": round(risk_exposure, 4)
        }
