"""
NEXUS Unified Risk Engine
Computes multi-dimensional, fully explainable risk scores across:
- Supplier Risk
- Inventory Risk
- Demand Risk
- Route Risk
- Warehouse Risk
- Network Overall Risk
"""

from typing import Dict, Any, List
import numpy as np
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import (
    Supplier, Inventory, Route, Warehouse, DemandZone
)
from backend.app.utils.logger import logger


class UnifiedRiskEngine:
    """
    Transparent risk aggregation and explainability engine.
    """

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def evaluate_supplier_risk(self, supplier: Supplier) -> Dict[str, Any]:
        """
        Supplier risk calculation based on empirical features.
        Score = 0.40 * (1 - on_time_rate) + 0.30 * (1 - quality_score) + 0.20 * (delays / 10) + 0.10 * (lead_time / 10)
        """
        otr_penalty = max(0.0, 1.0 - supplier.on_time_rate)
        qs_penalty = max(0.0, 1.0 - supplier.quality_score)
        delay_penalty = min(supplier.historical_delays / 12.0, 1.0)
        lt_penalty = min(supplier.lead_time / 10.0, 1.0)

        score = (0.40 * otr_penalty * 2.5) + (0.30 * qs_penalty * 5.0) + (0.20 * delay_penalty) + (0.10 * lt_penalty)
        score = round(float(np.clip(score, 0.05, 0.95)), 4)

        drivers = []
        if otr_penalty > 0.05:
            drivers.append(f"On-time delivery deficit ({(1-supplier.on_time_rate)*100:.1f}% late)")
        if qs_penalty > 0.03:
            drivers.append(f"Quality defect rate ({(1-supplier.quality_score)*100:.1f}%)")
        if supplier.historical_delays > 3:
            drivers.append(f"{supplier.historical_delays} recorded historical transit delays")

        return {
            "supplier_id": supplier.supplier_id,
            "name": supplier.supplier_name,
            "risk_score": score,
            "risk_level": "CRITICAL" if score > 0.60 else ("ELEVATED" if score > 0.30 else "LOW"),
            "drivers": drivers or ["Optimal supplier performance"]
        }

    def evaluate_inventory_risk(self, inv: Inventory) -> Dict[str, Any]:
        """
        Inventory stockout risk:
        Evaluates stock buffer vs reorder point and daily demand velocity.
        """
        coverage_days = inv.current_stock / max(inv.average_daily_demand, 0.1)
        deficit_ratio = max(0.0, (inv.reorder_point - inv.current_stock) / max(inv.reorder_point, 1.0))
        safety_deficit = max(0.0, (inv.safety_stock - inv.current_stock) / max(inv.safety_stock, 1.0))

        score = (0.50 * deficit_ratio) + (0.50 * safety_deficit)
        score = round(float(np.clip(score, 0.02, 0.99)), 4)

        drivers = []
        if inv.current_stock < inv.safety_stock:
            drivers.append("Current stock has breached safety stock threshold")
        elif inv.current_stock < inv.reorder_point:
            drivers.append("Current stock below reorder point")
        if coverage_days < 3.0:
            drivers.append(f"Critical inventory runway: only {coverage_days:.1f} days remaining")

        return {
            "warehouse_id": inv.warehouse_id,
            "product_id": inv.product_id,
            "risk_score": score,
            "coverage_days": round(coverage_days, 1),
            "drivers": drivers or ["Healthy buffer stock"]
        }

    def evaluate_route_risk(self, route: Route) -> Dict[str, Any]:
        """
        Route transit risk:
        Distance exposure, road congestion factor, base failure probability.
        """
        dist_factor = min(route.distance / 2500.0, 1.0)
        mode_factor = 0.25 if route.transport_mode == "ROAD" else 0.15
        base_risk = route.risk_level

        score = (0.50 * base_risk) + (0.30 * dist_factor) + (0.20 * mode_factor)
        score = round(float(np.clip(score, 0.02, 0.90)), 4)

        drivers = []
        if route.distance > 1200:
            drivers.append(f"Long-haul transit exposure ({route.distance:.0f} km)")
        if route.status != "OPEN":
            drivers.append(f"Route status alert: {route.status}")

        return {
            "route_id": route.route_id,
            "corridor": f"{route.origin} -> {route.destination}",
            "risk_score": score,
            "drivers": drivers or ["Normal corridor transit conditions"]
        }

    def evaluate_warehouse_risk(self, wh: Warehouse) -> Dict[str, Any]:
        """
        Warehouse operational risk:
        Capacity utilization stress, cost burden, status.
        """
        util = wh.current_utilization
        stress = max(0.0, (util - 0.75) / 0.25) if util > 0.75 else 0.0
        status_penalty = 0.8 if wh.status == "SHUTDOWN" else (0.4 if wh.status == "CONGESTED" else 0.0)

        score = (0.60 * stress) + (0.40 * status_penalty)
        score = round(float(np.clip(score, 0.05, 0.95)), 4)

        drivers = []
        if util > 0.85:
            drivers.append(f"Severe warehouse congestion: {util*100:.1f}% capacity utilized")
        if wh.status != "ACTIVE":
            drivers.append(f"Facility status: {wh.status}")

        return {
            "warehouse_id": wh.warehouse_id,
            "name": wh.name,
            "risk_score": score,
            "utilization": util,
            "drivers": drivers or ["Operating within nominal capacity bounds"]
        }

    def compute_network_risk_profile(self) -> Dict[str, Any]:
        """
        Aggregates all risk dimensions into an explainable network-wide risk index.
        """
        suppliers = self.db.query(Supplier).all()
        warehouses = self.db.query(Warehouse).all()
        routes = self.db.query(Route).all()
        inventories = self.db.query(Inventory).limit(100).all()

        sup_scores = [self.evaluate_supplier_risk(s)["risk_score"] for s in suppliers]
        wh_scores = [self.evaluate_warehouse_risk(w)["risk_score"] for w in warehouses]
        rt_scores = [self.evaluate_route_risk(r)["risk_score"] for r in routes]
        inv_scores = [self.evaluate_inventory_risk(i)["risk_score"] for i in inventories]

        avg_sup = float(np.mean(sup_scores)) if sup_scores else 0.1
        avg_wh = float(np.mean(wh_scores)) if wh_scores else 0.1
        avg_rt = float(np.mean(rt_scores)) if rt_scores else 0.1
        avg_inv = float(np.mean(inv_scores)) if inv_scores else 0.1

        # Composite Network Index: weighted combination
        composite_score = round(
            (0.30 * avg_sup) + (0.25 * avg_inv) + (0.25 * avg_rt) + (0.20 * avg_wh),
            4
        )

        return {
            "composite_network_risk_score": composite_score,
            "risk_status": "HIGH_RISK" if composite_score > 0.45 else ("MODERATE_RISK" if composite_score > 0.20 else "LOW_RISK"),
            "dimensions": {
                "supplier_risk": round(avg_sup, 4),
                "inventory_risk": round(avg_inv, 4),
                "route_risk": round(avg_rt, 4),
                "warehouse_risk": round(avg_wh, 4)
            },
            "top_vulnerable_suppliers": [
                self.evaluate_supplier_risk(s)
                for s in sorted(suppliers, key=lambda x: x.risk_score, reverse=True)[:3]
            ],
            "top_congested_warehouses": [
                self.evaluate_warehouse_risk(w)
                for w in sorted(warehouses, key=lambda x: x.current_utilization, reverse=True)[:3]
            ]
        }
