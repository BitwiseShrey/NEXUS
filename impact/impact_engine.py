"""
NEXUS Disruption Impact Propagation Engine
Traces failure propagation through the NetworkX supply chain graph:
Disruption -> Affected Entity -> Dependent Products -> Warehouses -> Routes -> Demand Zones -> Shortage & Service Level
"""

from typing import Dict, List, Any, Optional
import numpy as np
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import (
    Supplier, Product, Warehouse, Route, DemandZone, Inventory
)
from backend.app.utils.logger import logger
from digital_twin.network_graph import SupplyChainGraph


class ImpactEngine:
    """
    Simulates graph-based propagation of disruptions across the supply chain network.
    """

    def __init__(self, sc_graph: SupplyChainGraph = None, db: Session = None):
        self.graph = sc_graph
        self.db = db or SessionLocal()

    def analyze_supplier_disruption(
        self,
        supplier_id: str,
        capacity_reduction: float = 0.80,
        duration_days: int = 10
    ) -> Dict[str, Any]:
        """
        Calculates propagation impact when a supplier suffers capacity loss or factory shutdown.
        """
        supplier = self.db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
        if not supplier:
            return {"error": f"Supplier {supplier_id} not found"}

        # 1. Identify Dependent Products
        products = self.db.query(Product).filter(Product.primary_supplier_id == supplier_id).all()
        prod_ids = [p.product_id for p in products]
        criticality_breakdown = {
            "high_criticality_skus": [p.product_id for p in products if p.criticality == 3],
            "medium_criticality_skus": [p.product_id for p in products if p.criticality == 2],
            "low_criticality_skus": [p.product_id for p in products if p.criticality == 1],
        }

        # 2. Downstream routes from this supplier
        outbound_routes = self.db.query(Route).filter(Route.origin == supplier_id).all()
        affected_facilities = list(set([r.destination for r in outbound_routes]))

        # 3. Identify Dependent Warehouses and Current Stock Runway
        warehouses = self.db.query(Warehouse).filter(Warehouse.warehouse_id.in_(affected_facilities)).all()
        if not warehouses:
            # Fallback to all warehouses receiving these products
            inv_whs = self.db.query(Inventory.warehouse_id).filter(Inventory.product_id.in_(prod_ids)).distinct().all()
            wh_ids = [w[0] for w in inv_whs]
            warehouses = self.db.query(Warehouse).filter(Warehouse.warehouse_id.in_(wh_ids)).all()

        wh_impacts = []
        total_daily_runrate = 0.0
        for wh in warehouses:
            # Query inventories for affected products
            invs = self.db.query(Inventory).filter(
                Inventory.warehouse_id == wh.warehouse_id,
                Inventory.product_id.in_(prod_ids)
            ).all()
            for inv in invs:
                total_daily_runrate += inv.average_daily_demand
                runway = inv.current_stock / max(inv.average_daily_demand, 0.1)
                wh_impacts.append({
                    "warehouse_id": wh.warehouse_id,
                    "product_id": inv.product_id,
                    "current_stock": inv.current_stock,
                    "daily_demand": inv.average_daily_demand,
                    "stock_runway_days": round(runway, 1),
                    "stockout_expected": bool(runway < duration_days)
                })

        # 4. Impacted Demand Zones (using graph downstream search if available)
        downstream_zones = []
        if self.graph and supplier_id in self.graph.graph:
            dependents = self.graph.get_downstream_dependents(supplier_id)
            downstream_zones = [d for d in dependents if "ZONE" in d]
        if not downstream_zones:
            downstream_zones = [z.zone_id for z in self.db.query(DemandZone).limit(5).all()]

        # 5. Shortage & Service-Level Estimation
        daily_lost_capacity = supplier.capacity * capacity_reduction
        estimated_shortage_units = round(daily_lost_capacity * (duration_days / 30.0), 1)
        base_service_level = 0.98
        # Service level penalty proportional to shortage vs network run rate
        service_level_drop = round(min(0.35, (estimated_shortage_units / max(total_daily_runrate * duration_days, 100.0)) * 0.25), 3)
        projected_service_level = round(max(0.60, base_service_level - service_level_drop), 3)

        # 6. Alternative Supplier Options
        other_suppliers = self.db.query(Supplier).filter(
            Supplier.supplier_id != supplier_id,
            Supplier.product_categories.contains(supplier.product_categories.split()[0]),
            Supplier.status == "ACTIVE"
        ).all()
        alternative_suppliers = [{
            "supplier_id": s.supplier_id,
            "name": s.supplier_name,
            "location": s.location,
            "available_capacity": s.capacity,
            "unit_cost": s.unit_cost,
            "on_time_rate": s.on_time_rate,
            "risk_score": s.risk_score
        } for s in other_suppliers[:3]]

        logger.info(
            f"Impact analysis complete for {supplier_id}: {len(prod_ids)} products affected, "
            f"{estimated_shortage_units} unit shortage projected over {duration_days} days."
        )

        return {
            "disrupted_entity": {
                "id": supplier_id,
                "name": supplier.supplier_name,
                "type": "SUPPLIER",
                "location": supplier.location,
                "nominal_capacity": supplier.capacity,
                "capacity_reduction_rate": capacity_reduction,
                "duration_days": duration_days
            },
            "dependent_products_count": len(prod_ids),
            "dependent_products": [p.product_id for p in products],
            "criticality_breakdown": criticality_breakdown,
            "affected_warehouses_count": len(warehouses),
            "warehouse_runway_analysis": wh_impacts[:8],
            "affected_demand_zones": downstream_zones,
            "estimated_shortage_units": estimated_shortage_units,
            "baseline_service_level": base_service_level,
            "projected_service_level": projected_service_level,
            "service_level_deficit": round(base_service_level - projected_service_level, 3),
            "alternative_suppliers": alternative_suppliers
        }

    def analyze_warehouse_disruption(
        self,
        warehouse_id: str,
        duration_days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyzes the impact of a total or partial warehouse shutdown (e.g. flood, fire, strike).
        """
        wh = self.db.query(Warehouse).filter(Warehouse.warehouse_id == warehouse_id).first()
        if not wh:
            return {"error": f"Warehouse {warehouse_id} not found"}

        # Inventory immobilized
        inv_items = self.db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()
        total_stock = sum([i.current_stock for i in inv_items])
        daily_demand = sum([i.average_daily_demand for i in inv_items])

        # Routes severed
        inbound_routes = self.db.query(Route).filter(Route.destination == warehouse_id).all()
        outbound_routes = self.db.query(Route).filter(Route.origin == warehouse_id).all()

        # Potential shortage
        lost_fulfillment = round(daily_demand * duration_days, 1)

        return {
            "disrupted_entity": {
                "id": warehouse_id,
                "name": wh.name,
                "type": "WAREHOUSE",
                "location": wh.location,
                "capacity": wh.capacity
            },
            "immobilized_inventory_units": round(total_stock, 1),
            "severed_inbound_routes": [r.route_id for r in inbound_routes],
            "severed_outbound_routes": [r.route_id for r in outbound_routes],
            "projected_lost_fulfillment_units": lost_fulfillment,
            "estimated_service_level_drop": round(min(0.25, lost_fulfillment / 15000.0), 3)
        }

    def analyze_route_disruption(
        self,
        route_id: str,
        duration_days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyzes route blockade or severe congestion and discovers feasible reroutes.
        """
        route = self.db.query(Route).filter(Route.route_id == route_id).first()
        if not route:
            return {"error": f"Route {route_id} not found"}

        alt_paths = []
        if self.graph:
            alt_paths = self.graph.find_alternative_paths(
                origin=route.origin,
                destination=route.destination,
                blocked_edges={(route.origin, route.destination)},
                max_paths=2
            )

        return {
            "disrupted_route": {
                "route_id": route.route_id,
                "corridor": f"{route.origin} -> {route.destination}",
                "mode": route.transport_mode,
                "distance_km": route.distance,
                "transit_time_days": route.transit_time
            },
            "duration_days": duration_days,
            "reroute_options": alt_paths,
            "can_reroute": len(alt_paths) > 0,
            "extra_transit_days": round(alt_paths[0]["total_transit_days"] - route.transit_time, 2) if alt_paths else None
        }
