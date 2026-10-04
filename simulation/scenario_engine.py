"""
NEXUS Scenario Simulation Engine
Allows non-destructive simulation of stress events:
- Supplier failure
- Route disruption
- Demand spikes
- Warehouse shutdown
- Combined multi-hazard disruptions
"""

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import (
    Supplier, Warehouse, Route, DemandZone, Product
)
from backend.app.utils.logger import logger


class ScenarioType(str, Enum):
    SUPPLIER_FAILURE = "SUPPLIER_FAILURE"
    ROUTE_DISRUPTION = "ROUTE_DISRUPTION"
    DEMAND_SPIKE = "DEMAND_SPIKE"
    WAREHOUSE_SHUTDOWN = "WAREHOUSE_SHUTDOWN"
    COMBINED_DISRUPTION = "COMBINED_DISRUPTION"


@dataclass
class SimulationState:
    """Ephemeral digital twin state during scenario execution."""
    suppliers: Dict[str, Dict[str, Any]]
    warehouses: Dict[str, Dict[str, Any]]
    routes: Dict[str, Dict[str, Any]]
    demand_zones: Dict[str, Dict[str, Any]]
    active_disruptions: List[Dict[str, Any]] = field(default_factory=list)


class ScenarioEngine:
    """
    Simulates operational shocks and computes modified network capacities without modifying persistent DB.
    """

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self.base_state = self._capture_base_state()

    def _capture_base_state(self) -> SimulationState:
        """Captures a clean in-memory snapshot of all active entities."""
        sups = {s.supplier_id: {
            "supplier_id": s.supplier_id,
            "name": s.supplier_name,
            "capacity": s.capacity,
            "unit_cost": s.unit_cost,
            "lead_time": s.lead_time,
            "on_time_rate": s.on_time_rate,
            "risk_score": s.risk_score,
            "status": s.status,
            "product_categories": s.product_categories
        } for s in self.db.query(Supplier).all()}

        whs = {w.warehouse_id: {
            "warehouse_id": w.warehouse_id,
            "name": w.name,
            "capacity": w.capacity,
            "utilization": w.current_utilization,
            "operating_cost": w.operating_cost,
            "status": w.status
        } for w in self.db.query(Warehouse).all()}

        rts = {r.route_id: {
            "route_id": r.route_id,
            "origin": r.origin,
            "destination": r.destination,
            "distance": r.distance,
            "transit_time": r.transit_time,
            "cost": r.transportation_cost,
            "capacity": r.capacity,
            "status": r.status
        } for r in self.db.query(Route).all()}

        dzs = {d.zone_id: {
            "zone_id": d.zone_id,
            "name": d.name,
            "product_id": d.product_id,
            "demand": d.historical_demand,
            "growth": d.demand_growth
        } for d in self.db.query(DemandZone).all()}

        return SimulationState(suppliers=sups, warehouses=whs, routes=rts, demand_zones=dzs)

    def run_scenario(
        self,
        scenario_type: ScenarioType,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a simulation on a fresh in-memory clone of the digital twin.
        """
        sim_state = deepcopy(self.base_state)
        applied_disruptions = []

        logger.info(f"Running scenario simulation: {scenario_type.value} with params {parameters}")

        # 1. Supplier Failure Shock
        if scenario_type in [ScenarioType.SUPPLIER_FAILURE, ScenarioType.COMBINED_DISRUPTION]:
            sup_id = parameters.get("supplier_id", "SUP_001")
            cap_reduction = float(parameters.get("capacity_reduction", 0.80))
            duration = int(parameters.get("duration_days", 10))

            if sup_id in sim_state.suppliers:
                orig_cap = sim_state.suppliers[sup_id]["capacity"]
                new_cap = orig_cap * (1.0 - cap_reduction)
                sim_state.suppliers[sup_id]["capacity"] = new_cap
                sim_state.suppliers[sup_id]["status"] = "DISRUPTED"
                sim_state.suppliers[sup_id]["risk_score"] = 0.85
                applied_disruptions.append({
                    "type": "SUPPLIER_FAILURE",
                    "entity_id": sup_id,
                    "original_capacity": orig_cap,
                    "simulated_capacity": new_cap,
                    "capacity_lost": orig_cap - new_cap,
                    "duration_days": duration
                })

        # 2. Route Disruption Shock
        if scenario_type in [ScenarioType.ROUTE_DISRUPTION, ScenarioType.COMBINED_DISRUPTION]:
            route_id = parameters.get("route_id", "RT_0001")
            if route_id in sim_state.routes:
                sim_state.routes[route_id]["status"] = "BLOCKED"
                sim_state.routes[route_id]["capacity"] = 0.0
                applied_disruptions.append({
                    "type": "ROUTE_DISRUPTION",
                    "entity_id": route_id,
                    "corridor": f"{sim_state.routes[route_id]['origin']} -> {sim_state.routes[route_id]['destination']}",
                    "status": "BLOCKED"
                })

        # 3. Demand Spike Shock
        if scenario_type in [ScenarioType.DEMAND_SPIKE, ScenarioType.COMBINED_DISRUPTION]:
            spike_multiplier = float(parameters.get("demand_spike_percent", 0.70))  # e.g. +70%
            zone_id = parameters.get("zone_id")  # None means network-wide spike
            affected_zones = [zone_id] if zone_id else list(sim_state.demand_zones.keys())[:10]

            total_added_demand = 0.0
            for zid in affected_zones:
                if zid in sim_state.demand_zones:
                    orig_d = sim_state.demand_zones[zid]["demand"]
                    new_d = orig_d * (1.0 + spike_multiplier)
                    sim_state.demand_zones[zid]["demand"] = new_d
                    total_added_demand += (new_d - orig_d)

            applied_disruptions.append({
                "type": "DEMAND_SPIKE",
                "affected_zones_count": len(affected_zones),
                "spike_factor": 1.0 + spike_multiplier,
                "additional_demand_units": round(total_added_demand, 1)
            })

        # 4. Warehouse Shutdown Shock
        if scenario_type in [ScenarioType.WAREHOUSE_SHUTDOWN, ScenarioType.COMBINED_DISRUPTION]:
            wh_id = parameters.get("warehouse_id", "WH_01")
            if wh_id in sim_state.warehouses:
                sim_state.warehouses[wh_id]["status"] = "SHUTDOWN"
                sim_state.warehouses[wh_id]["capacity"] = 0.0
                # Block inbound and outbound routes to this warehouse
                for r_id, r_data in sim_state.routes.items():
                    if r_data["origin"] == wh_id or r_data["destination"] == wh_id:
                        r_data["status"] = "BLOCKED"
                        r_data["capacity"] = 0.0

                applied_disruptions.append({
                    "type": "WAREHOUSE_SHUTDOWN",
                    "entity_id": wh_id,
                    "status": "SHUTDOWN"
                })

        # Calculate simulated network summary
        total_demand = sum([dz["demand"] for dz in sim_state.demand_zones.values()])
        total_supply_cap = sum([s["capacity"] for s in sim_state.suppliers.values() if s["status"] != "DISRUPTED"])
        net_balance = total_supply_cap - total_demand

        return {
            "scenario_type": scenario_type.value,
            "parameters": parameters,
            "applied_disruptions": applied_disruptions,
            "simulated_network_state": {
                "total_demand_units": round(total_demand, 1),
                "total_available_supplier_capacity": round(total_supply_cap, 1),
                "net_capacity_balance": round(net_balance, 1),
                "severed_routes_count": len([r for r in sim_state.routes.values() if r["status"] == "BLOCKED"]),
                "compromised_suppliers_count": len([s for s in sim_state.suppliers.values() if s["status"] == "DISRUPTED"]),
            },
            "state_object": sim_state
        }
