"""
NEXUS Optimization Engine (Google OR-Tools)
Solves multi-echelon network allocation:
Minimize: Procurement Cost + Freight Cost + Holding Cost + Shortage Penalty + Risk Penalty
Subject to: Supplier Capacity, Warehouse Capacity, Flow Conservation, Demand Balance, Corridor Feasibility.
"""

import time
from typing import Dict, Any, List, Tuple
import numpy as np
from ortools.linear_solver import pywraplp

from backend.app.utils.logger import logger
from simulation.scenario_engine import SimulationState
from optimization.baseline_optimizer import BaselineOptimizer


class SupplyChainOptimizer:
    """
    Formulates and solves multi-echelon linear optimization using Google OR-Tools.
    """

    def __init__(self, risk_aversion_weight: float = 50.0, shortage_penalty_unit: float = 350.0):
        self.risk_weight = risk_aversion_weight
        self.shortage_penalty = shortage_penalty_unit

    def solve(self, sim_state: SimulationState) -> Dict[str, Any]:
        """
        Solves the supply chain allocation problem given a simulated network state.
        """
        start_time = time.time()
        logger.info("Initializing Google OR-Tools linear solver (GLOP)...")

        # Create GLOP solver
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if not solver:
            logger.error("Could not create OR-Tools GLOP solver instance.")
            return {"status": "SOLVER_UNAVAILABLE"}

        infinity = solver.infinity()

        suppliers = list(sim_state.suppliers.keys())
        warehouses = list(sim_state.warehouses.keys())
        demand_zones = list(sim_state.demand_zones.keys())

        # Blocked routes lookup
        blocked_routes = {
            (r["origin"], r["destination"])
            for r in sim_state.routes.values()
            if r.get("status") == "BLOCKED"
        }

        # -------------------------------------------------------------
        # Decision Variables
        # -------------------------------------------------------------
        # Flow from Supplier s to Warehouse w
        x = {}
        for s in suppliers:
            for w in warehouses:
                # If warehouse is shutdown or corridor blocked, capacity is 0
                is_blocked = (s, w) in blocked_routes or sim_state.warehouses[w].get("status") == "SHUTDOWN"
                upper_bound = 0.0 if is_blocked else sim_state.suppliers[s]["capacity"]
                x[s, w] = solver.NumVar(0.0, upper_bound, f"flow_sup_{s}_to_wh_{w}")

        # Flow from Warehouse w to Demand Zone d
        y = {}
        for w in warehouses:
            for d in demand_zones:
                is_blocked = (w, d) in blocked_routes or sim_state.warehouses[w].get("status") == "SHUTDOWN"
                upper_bound = 0.0 if is_blocked else sim_state.warehouses[w]["capacity"]
                y[w, d] = solver.NumVar(0.0, upper_bound, f"flow_wh_{w}_to_dz_{d}")

        # Unmet demand (shortage) at Demand Zone d
        u = {}
        for d in demand_zones:
            dem = sim_state.demand_zones[d]["demand"]
            u[d] = solver.NumVar(0.0, dem, f"shortage_dz_{d}")

        # -------------------------------------------------------------
        # Constraints
        # -------------------------------------------------------------
        # 1. Supplier Capacity Constraints: sum_w x[s, w] <= Cap[s]
        for s in suppliers:
            cap_s = sim_state.suppliers[s]["capacity"]
            solver.Add(solver.Sum([x[s, w] for w in warehouses]) <= cap_s)

        # 2. Warehouse Inbound Capacity: sum_s x[s, w] <= Cap[w]
        for w in warehouses:
            cap_w = sim_state.warehouses[w]["capacity"]
            solver.Add(solver.Sum([x[s, w] for s in suppliers]) <= cap_w)

        # 3. Warehouse Flow Conservation: Outbound <= Inbound
        for w in warehouses:
            inbound = solver.Sum([x[s, w] for s in suppliers])
            outbound = solver.Sum([y[w, d] for d in demand_zones])
            solver.Add(outbound <= inbound)

        # 4. Demand Zone Satisfaction: sum_w y[w, d] + u[d] == Demand[d]
        for d in demand_zones:
            dem_d = sim_state.demand_zones[d]["demand"]
            solver.Add(solver.Sum([y[w, d] for w in warehouses]) + u[d] == dem_d)

        # -------------------------------------------------------------
        # Objective Function
        # -------------------------------------------------------------
        objective = solver.Objective()

        # Cost components
        for s in suppliers:
            unit_proc = sim_state.suppliers[s]["unit_cost"]
            risk_penalty = self.risk_weight * sim_state.suppliers[s]["risk_score"]
            for w in warehouses:
                # Approx freight cost per unit
                freight_sw = 15.0
                cost_sw = unit_proc + freight_sw + risk_penalty
                objective.SetCoefficient(x[s, w], cost_sw)

        for w in warehouses:
            holding_cost = 8.0
            for d in demand_zones:
                freight_wd = 20.0
                cost_wd = holding_cost + freight_wd
                objective.SetCoefficient(y[w, d], cost_wd)

        # Shortage penalty
        for d in demand_zones:
            objective.SetCoefficient(u[d], self.shortage_penalty)

        objective.SetMinimization()

        # -------------------------------------------------------------
        # Solve
        # -------------------------------------------------------------
        status = solver.Solve()
        runtime = round(time.time() - start_time, 4)

        if status not in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            logger.warning(f"OR-Tools solver terminated with status code {status}")
            return {
                "status": "INFEASIBLE",
                "runtime_seconds": runtime
            }

        # Calculate solution breakdown
        total_procurement = 0.0
        total_freight = 0.0
        total_shortage_units = 0.0
        total_fulfilled_units = 0.0
        active_allocations = []

        for s in suppliers:
            for w in warehouses:
                val = x[s, w].solution_value()
                if val > 1.0:
                    total_procurement += val * sim_state.suppliers[s]["unit_cost"]
                    total_freight += val * 15.0
                    active_allocations.append({
                        "from": s,
                        "to": w,
                        "units": round(val, 1),
                        "type": "SUPPLIER_TO_WAREHOUSE"
                    })

        for w in warehouses:
            for d in demand_zones:
                val = y[w, d].solution_value()
                if val > 1.0:
                    total_fulfilled_units += val
                    total_freight += val * 20.0
                    active_allocations.append({
                        "from": w,
                        "to": d,
                        "units": round(val, 1),
                        "type": "WAREHOUSE_TO_DEMAND_ZONE"
                    })

        for d in demand_zones:
            val = u[d].solution_value()
            total_shortage_units += val

        total_demand = sum([dz["demand"] for dz in sim_state.demand_zones.values()])
        service_level = round(float(total_fulfilled_units / max(total_demand, 1.0)), 4)
        shortage_penalty_cost = total_shortage_units * self.shortage_penalty
        total_cost = round(objective.Value(), 2)

        logger.info(
            f"Optimization finished in {runtime}s. Total Cost: INR {total_cost:,.2f}, "
            f"Service Level: {service_level*100:.1f}%, Shortages: {total_shortage_units:.1f} units"
        )

        return {
            "mode": "NEXUS_ORTOOLS_OPTIMIZED",
            "status": "OPTIMAL",
            "runtime_seconds": runtime,
            "total_cost": total_cost,
            "service_level": service_level,
            "total_demand": round(total_demand, 1),
            "total_fulfilled": round(total_fulfilled_units, 1),
            "total_shortages": round(total_shortage_units, 1),
            "procurement_cost": round(total_procurement, 2),
            "transportation_cost": round(total_freight, 2),
            "penalty_cost": round(shortage_penalty_cost, 2),
            "allocations_count": len(active_allocations),
            "top_allocations": active_allocations[:10]
        }

    def compare_with_baseline(self, sim_state: SimulationState) -> Dict[str, Any]:
        """
        Executes both baseline heuristic and OR-Tools optimization, calculating empirical value-add.
        """
        baseline_res = BaselineOptimizer.solve(sim_state, shortage_penalty_per_unit=self.shortage_penalty)
        optimized_res = self.solve(sim_state)

        # Calculate differential gains
        cost_diff = baseline_res["total_cost"] - optimized_res["total_cost"]
        cost_pct = round((cost_diff / max(baseline_res["total_cost"], 1.0)) * 100, 2)

        shortage_reduction = baseline_res["total_shortages"] - optimized_res["total_shortages"]
        sl_gain = round((optimized_res["service_level"] - baseline_res["service_level"]) * 100, 2)

        logger.info(
            f"Baseline vs NEXUS Comparison: Cost Saved: INR {cost_diff:,.2f} ({cost_pct}%), "
            f"Shortage Reduced: {shortage_reduction:.1f} units, Service Level Delta: +{sl_gain}%"
        )

        return {
            "baseline": baseline_res,
            "nexus_optimized": optimized_res,
            "impact_comparison": {
                "cost_saved_inr": round(cost_diff, 2),
                "cost_reduction_percent": cost_pct,
                "shortage_reduction_units": round(shortage_reduction, 1),
                "service_level_improvement_percentage_points": sl_gain,
                "is_nexus_superior": bool(cost_diff > 0 or sl_gain > 0)
            }
        }
