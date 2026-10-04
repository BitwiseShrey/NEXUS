"""
NEXUS Relational Database ORM Models
Defines all digital twin supply chain entities, operational tables, ML logs, and optimization outputs.
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    ForeignKey, Text, Index, JSON
)
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(String(50), primary_key=True, index=True)
    supplier_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    product_categories = Column(String(255), nullable=False)
    capacity = Column(Float, nullable=False)
    lead_time = Column(Float, nullable=False)  # in days
    unit_cost = Column(Float, nullable=False)
    on_time_rate = Column(Float, nullable=False, default=0.95)
    quality_score = Column(Float, nullable=False, default=0.98)
    historical_delays = Column(Integer, default=0)
    risk_score = Column(Float, default=0.1)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, DISRUPTED, SUSPENDED

    # Relationships
    products = relationship("Product", back_populates="supplier")

    __table_args__ = (
        Index("idx_supplier_risk", "risk_score"),
        Index("idx_supplier_status", "status"),
    )


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    unit_cost = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    criticality = Column(Integer, default=1)  # 1: Low, 2: Medium, 3: High/Critical
    primary_supplier_id = Column(String(50), ForeignKey("suppliers.supplier_id"), nullable=True)

    supplier = relationship("Supplier", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")


class ProductionUnit(Base):
    __tablename__ = "production_units"

    production_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    operational_status = Column(String(20), default="OPERATIONAL")  # OPERATIONAL, RESTRICTED, OFFLINE


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    current_utilization = Column(Float, default=0.0)  # Percentage 0.0 - 1.0
    operating_cost = Column(Float, nullable=False, default=1000.0)  # Daily operating cost
    status = Column(String(20), default="ACTIVE")  # ACTIVE, CONGESTED, SHUTDOWN

    inventories = relationship("Inventory", back_populates="warehouse")


class DistributionHub(Base):
    __tablename__ = "distribution_hubs"

    hub_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    status = Column(String(20), default="ACTIVE")


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(String(50), ForeignKey("warehouses.warehouse_id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False, index=True)
    current_stock = Column(Float, default=0.0)
    reserved_stock = Column(Float, default=0.0)
    reorder_point = Column(Float, default=100.0)
    safety_stock = Column(Float, default=50.0)
    average_daily_demand = Column(Float, default=20.0)
    stockout_risk = Column(Float, default=0.05)  # 0.0 - 1.0 probability

    warehouse = relationship("Warehouse", back_populates="inventories")
    product = relationship("Product", back_populates="inventories")

    __table_args__ = (
        Index("idx_warehouse_product", "warehouse_id", "product_id", unique=True),
    )


class DemandZone(Base):
    __tablename__ = "demand_zones"

    zone_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=True)
    historical_demand = Column(Float, default=0.0)
    forecast_demand = Column(Float, default=0.0)
    demand_growth = Column(Float, default=0.05)


class Route(Base):
    __tablename__ = "routes"

    route_id = Column(String(50), primary_key=True, index=True)
    origin = Column(String(100), nullable=False, index=True)
    destination = Column(String(100), nullable=False, index=True)
    origin_type = Column(String(30), default="FACILITY")  # SUPPLIER, WAREHOUSE, HUB, DEMAND_ZONE
    destination_type = Column(String(30), default="FACILITY")
    distance = Column(Float, nullable=False)  # in km
    transport_mode = Column(String(30), default="ROAD")  # ROAD, RAIL, AIR
    transit_time = Column(Float, nullable=False)  # in days
    transportation_cost = Column(Float, nullable=False)  # per unit or total
    capacity = Column(Float, nullable=False)  # maximum units per day
    risk_level = Column(Float, default=0.05)  # 0.0 - 1.0
    status = Column(String(20), default="OPEN")  # OPEN, CONGESTED, BLOCKED


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True, index=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    expected_delivery = Column(DateTime, nullable=False)
    actual_delivery = Column(DateTime, nullable=True)
    status = Column(String(30), default="DELIVERED")  # PENDING, IN_TRANSIT, DELIVERED, LATE, CANCELED


class Disruption(Base):
    __tablename__ = "disruptions"

    disruption_id = Column(String(50), primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # WEATHER, STRIKE, SUPPLIER_FAILURE, ACCIDENT, PORT_CONGESTION
    location = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    severity = Column(Float, nullable=False)  # 0.0 - 1.0
    affected_supplier = Column(String(50), ForeignKey("suppliers.supplier_id"), nullable=True)
    affected_warehouse = Column(String(50), ForeignKey("warehouses.warehouse_id"), nullable=True)
    affected_route = Column(String(50), ForeignKey("routes.route_id"), nullable=True)
    historical_impact = Column(Text, nullable=True)


class RiskEvent(Base):
    __tablename__ = "risk_events"

    event_id = Column(String(50), primary_key=True, index=True)
    entity_type = Column(String(30), nullable=False)  # SUPPLIER, ROUTE, WAREHOUSE, NETWORK
    entity_id = Column(String(50), nullable=False, index=True)
    risk_type = Column(String(50), nullable=False)
    risk_score = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    severity = Column(Float, nullable=False)
    features = Column(JSON, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)


class Forecast(Base):
    __tablename__ = "forecasts"

    forecast_id = Column(String(50), primary_key=True, index=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False, index=True)
    location_id = Column(String(50), nullable=True)
    model_name = Column(String(50), nullable=False)
    horizon_days = Column(Integer, default=30)
    historical_window = Column(Integer, default=90)
    forecast_values = Column(JSON, nullable=False)
    metrics = Column(JSON, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)


class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    run_id = Column(String(50), primary_key=True, index=True)
    scenario_name = Column(String(100), nullable=False)
    objective_type = Column(String(50), default="MINIMIZE_TOTAL_COST")
    status = Column(String(30), default="OPTIMAL")
    total_cost = Column(Float, nullable=False)
    service_level = Column(Float, nullable=False)  # 0.0 - 1.0
    shortages_total = Column(Float, default=0.0)
    procurement_cost = Column(Float, default=0.0)
    transportation_cost = Column(Float, default=0.0)
    penalty_cost = Column(Float, default=0.0)
    runtime_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    recommendations = relationship("Recommendation", back_populates="optimization_run")


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(String(50), primary_key=True, index=True)
    run_id = Column(String(50), ForeignKey("optimization_runs.run_id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    reason = Column(Text, nullable=False)
    affected_entities = Column(JSON, nullable=False)
    action_type = Column(String(50), nullable=False)  # REROUTE, REALLOCATE_SUPPLIER, BUFFER_INVENTORY, EXPEDITE
    expected_benefit = Column(Text, nullable=False)
    expected_cost = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.9)
    created_at = Column(DateTime, default=datetime.utcnow)

    optimization_run = relationship("OptimizationRun", back_populates="recommendations")
