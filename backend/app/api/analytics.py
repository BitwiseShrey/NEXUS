"""
NEXUS Analytics and GIS Endpoints
Provides operational KPIs and spatial GeoJSON facility coordinates for mapping.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Supplier, ProductionUnit, Warehouse, DistributionHub, DemandZone
from digital_twin.analytics import SupplyChainAnalytics

router = APIRouter(prefix="/analytics", tags=["Operational Analytics & GIS"])


@router.get("/summary", summary="Executive Operational KPI Summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Returns baseline network KPIs across suppliers, inventory health, transit routes, and fulfillment.
    """
    analytics = SupplyChainAnalytics(db)
    return analytics.get_network_executive_summary()


@router.get("/gis/facilities", summary="GeoJSON Spatial Facilities Mapping")
def get_gis_facilities(db: Session = Depends(get_db)):
    """
    Exposes Indian digital twin facilities in GeoJSON FeatureCollection format for future GIS map rendering.
    """
    features = []

    # Suppliers
    for s in db.query(Supplier).all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [s.longitude, s.latitude]},
            "properties": {
                "id": s.supplier_id,
                "name": s.supplier_name,
                "type": "SUPPLIER",
                "location": s.location,
                "capacity": s.capacity,
                "risk_score": s.risk_score,
                "status": s.status
            }
        })

    # Warehouses
    for w in db.query(Warehouse).all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [w.longitude, w.latitude]},
            "properties": {
                "id": w.warehouse_id,
                "name": w.name,
                "type": "WAREHOUSE",
                "location": w.location,
                "capacity": w.capacity,
                "utilization": w.current_utilization,
                "status": w.status
            }
        })

    # Production Units
    for p in db.query(ProductionUnit).all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [p.longitude, p.latitude]},
            "properties": {
                "id": p.production_id,
                "name": p.name,
                "type": "PRODUCTION",
                "location": p.location,
                "capacity": p.capacity,
                "status": p.operational_status
            }
        })

    # Distribution Hubs
    for h in db.query(DistributionHub).all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [h.longitude, h.latitude]},
            "properties": {
                "id": h.hub_id,
                "name": h.name,
                "type": "HUB",
                "location": h.location,
                "capacity": h.capacity,
                "status": h.status
            }
        })

    # Demand Zones
    for d in db.query(DemandZone).all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [d.longitude, d.latitude]},
            "properties": {
                "id": d.zone_id,
                "name": d.name,
                "type": "DEMAND_ZONE",
                "region": d.region,
                "historical_demand": d.historical_demand,
                "forecast_demand": d.forecast_demand
            }
        })

    return {
        "type": "FeatureCollection",
        "total_features": len(features),
        "features": features
    }
