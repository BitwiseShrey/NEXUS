"""
NEXUS Baseline Analytics Engine
Calculates operational supply chain KPIs, descriptive statistics, supplier performance,
inventory health, and route statistics prior to predictive modeling.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import (
    Supplier, Product, Warehouse, Route, Order, Inventory, DemandZone
)
from backend.app.utils.logger import logger


class SupplyChainAnalytics:
    """
    Computes baseline supply-chain descriptive statistics and operational KPIs.
    """

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def get_supplier_kpis(self) -> Dict[str, Any]:
        """Calculates supplier reliability, lead-time volatility, and quality score statistics."""
        suppliers = self.db.query(Supplier).all()
        if not suppliers:
            return {}

        df_sups = pd.DataFrame([{
            "id": s.supplier_id,
            "name": s.supplier_name,
            "on_time_rate": s.on_time_rate,
            "quality_score": s.quality_score,
            "lead_time": s.lead_time,
            "risk_score": s.risk_score,
            "capacity": s.capacity,
            "delays": s.historical_delays
        } for s in suppliers])

        return {
            "total_suppliers": len(df_sups),
            "mean_on_time_rate": round(float(df_sups["on_time_rate"].mean()), 4),
            "min_on_time_rate": round(float(df_sups["on_time_rate"].min()), 4),
            "mean_quality_score": round(float(df_sups["quality_score"].mean()), 4),
            "mean_lead_time_days": round(float(df_sups["lead_time"].mean()), 2),
            "mean_risk_score": round(float(df_sups["risk_score"].mean()), 4),
            "total_capacity_units": float(df_sups["capacity"].sum()),
            "high_risk_suppliers_count": int((df_sups["risk_score"] > 0.25).sum())
        }

    def get_inventory_kpis(self) -> Dict[str, Any]:
        """Calculates stock levels, stockout risks, safety stock adherence, and valuation."""
        inv_items = self.db.query(Inventory, Product).join(Product, Inventory.product_id == Product.product_id).all()
        if not inv_items:
            return {}

        rows = []
        for inv, prod in inv_items:
            valuation = inv.current_stock * prod.unit_cost
            stock_coverage = inv.current_stock / max(inv.average_daily_demand, 0.1)
            rows.append({
                "warehouse_id": inv.warehouse_id,
                "product_id": inv.product_id,
                "current_stock": inv.current_stock,
                "reorder_point": inv.reorder_point,
                "safety_stock": inv.safety_stock,
                "stockout_risk": inv.stockout_risk,
                "valuation": valuation,
                "stock_coverage_days": stock_coverage
            })

        df_inv = pd.DataFrame(rows)

        return {
            "total_skus_tracked": len(df_inv),
            "total_inventory_valuation_inr": round(float(df_inv["valuation"].sum()), 2),
            "mean_stockout_risk": round(float(df_inv["stockout_risk"].mean()), 4),
            "critical_stockout_skus": int((df_inv["stockout_risk"] > 0.30).sum()),
            "mean_stock_coverage_days": round(float(df_inv["stock_coverage_days"].mean()), 1),
            "below_reorder_point_count": int((df_inv["current_stock"] < df_inv["reorder_point"]).sum())
        }

    def get_route_kpis(self) -> Dict[str, Any]:
        """Calculates transit network statistics across road and rail corridors."""
        routes = self.db.query(Route).all()
        if not routes:
            return {}

        df_routes = pd.DataFrame([{
            "id": r.route_id,
            "mode": r.transport_mode,
            "distance": r.distance,
            "transit_time": r.transit_time,
            "cost": r.transportation_cost,
            "risk_level": r.risk_level,
            "status": r.status
        } for r in routes])

        return {
            "total_routes": len(df_routes),
            "mean_distance_km": round(float(df_routes["distance"].mean()), 1),
            "mean_transit_days": round(float(df_routes["transit_time"].mean()), 2),
            "mean_cost_per_shipment": round(float(df_routes["cost"].mean()), 2),
            "routes_by_mode": df_routes["mode"].value_counts().to_dict(),
            "mean_route_risk": round(float(df_routes["risk_level"].mean()), 4),
            "open_routes_percentage": round(float((df_routes["status"] == "OPEN").mean() * 100), 1)
        }

    def get_order_fulfillment_kpis(self) -> Dict[str, Any]:
        """Calculates order fulfillment statistics, on-time delivery rate, and volume."""
        orders = self.db.query(Order).limit(10000).all()
        if not orders:
            return {}

        df_orders = pd.DataFrame([{
            "id": o.order_id,
            "quantity": o.quantity,
            "status": o.status
        } for o in orders])

        total_orders = len(df_orders)
        on_time = (df_orders["status"] == "DELIVERED").sum()
        late = (df_orders["status"] == "LATE").sum()

        return {
            "sample_orders_analyzed": total_orders,
            "on_time_delivery_rate": round(float(on_time / total_orders), 4),
            "late_delivery_rate": round(float(late / total_orders), 4),
            "mean_order_quantity": round(float(df_orders["quantity"].mean()), 1),
            "median_order_quantity": round(float(df_orders["quantity"].median()), 1)
        }

    def get_network_executive_summary(self) -> Dict[str, Any]:
        """Aggregates all baseline KPI domains into an executive status dashboard."""
        return {
            "suppliers": self.get_supplier_kpis(),
            "inventory": self.get_inventory_kpis(),
            "routes": self.get_route_kpis(),
            "fulfillment": self.get_order_fulfillment_kpis()
        }
