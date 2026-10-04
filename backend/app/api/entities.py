"""
NEXUS Digital Twin Entity Endpoints
Provides structured access to facilities, routes, inventory, and network graph topology.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import (
    Supplier, Product, Warehouse, Route, Inventory, DemandZone, DistributionHub
)
from backend.app.schemas.api_schemas import (
    SupplierResponse, ProductResponse, WarehouseResponse, RouteResponse,
    InventoryResponse, DemandZoneResponse, NetworkSummaryResponse
)

router = APIRouter(tags=["Digital Twin Entities"])


@router.get("/suppliers", response_model=List[SupplierResponse], summary="List all suppliers")
def get_suppliers(
    status: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Supplier)
    if status:
        query = query.filter(Supplier.status == status)
    if category:
        query = query.filter(Supplier.product_categories.contains(category))
    return query.limit(limit).all()


@router.get("/products", response_model=List[ProductResponse], summary="List catalog products")
def get_products(
    category: Optional[str] = None,
    criticality: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if criticality:
        query = query.filter(Product.criticality == criticality)
    return query.limit(limit).all()


@router.get("/warehouses", response_model=List[WarehouseResponse], summary="List fulfillment warehouses")
def get_warehouses(
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Warehouse)
    if status:
        query = query.filter(Warehouse.status == status)
    return query.limit(limit).all()


@router.get("/routes", response_model=List[RouteResponse], summary="List logistics transit corridors")
def get_routes(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    mode: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(Route)
    if origin:
        query = query.filter(Route.origin == origin)
    if destination:
        query = query.filter(Route.destination == destination)
    if mode:
        query = query.filter(Route.transport_mode == mode)
    if status:
        query = query.filter(Route.status == status)
    return query.limit(limit).all()


@router.get("/inventory", response_model=List[InventoryResponse], summary="List warehouse stock levels")
def get_inventory(
    warehouse_id: Optional[str] = None,
    product_id: Optional[str] = None,
    critical_only: bool = False,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(Inventory)
    if warehouse_id:
        query = query.filter(Inventory.warehouse_id == warehouse_id)
    if product_id:
        query = query.filter(Inventory.product_id == product_id)
    if critical_only:
        query = query.filter(Inventory.stockout_risk > 0.25)
    return query.limit(limit).all()


@router.get("/demand", response_model=List[DemandZoneResponse], summary="List regional demand zones")
def get_demand_zones(
    region: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(DemandZone)
    if region:
        query = query.filter(DemandZone.region == region)
    return query.limit(limit).all()


@router.get("/network", response_model=NetworkSummaryResponse, summary="Network graph topology summary")
def get_network_summary(db: Session = Depends(get_db)):
    n_sups = db.query(Supplier).count()
    n_prods = db.query(Product).count()
    n_whs = db.query(Warehouse).count()
    n_hubs = db.query(DistributionHub).count()
    n_dzs = db.query(DemandZone).count()
    n_routes = db.query(Route).count()

    total_nodes = n_sups + 8 + n_whs + n_hubs + n_dzs
    return {
        "total_nodes": total_nodes,
        "total_edges": n_routes,
        "nodes_by_type": {
            "SUPPLIER": n_sups,
            "PRODUCTION": 8,
            "WAREHOUSE": n_whs,
            "HUB": n_hubs,
            "DEMAND_ZONE": n_dzs
        },
        "status": "OPERATIONAL"
    }
