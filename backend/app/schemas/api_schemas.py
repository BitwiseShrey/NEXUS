"""
NEXUS Pydantic API Schemas
Defines request and response data contracts, validation rules, and Swagger examples.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# -------------------------------------------------------------
# Base Entity Schemas
# -------------------------------------------------------------

class SupplierResponse(BaseModel):
    supplier_id: str = Field(..., example="SUP_001")
    supplier_name: str = Field(..., example="Tata AutoComp Components")
    location: str = Field(..., example="Pune (Chakan), Maharashtra")
    latitude: float = Field(..., example=18.7606)
    longitude: float = Field(..., example=73.8617)
    product_categories: str = Field(..., example="Automotive")
    capacity: float = Field(..., example=12000.0)
    lead_time: float = Field(..., example=4.0)
    unit_cost: float = Field(..., example=145.0)
    on_time_rate: float = Field(..., example=0.94)
    quality_score: float = Field(..., example=0.97)
    risk_score: float = Field(..., example=0.12)
    status: str = Field(..., example="ACTIVE")

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    product_id: str = Field(..., example="PROD_ITEM_001")
    product_name: str = Field(..., example="Automotive SKU-001")
    category: str = Field(..., example="Automotive")
    unit_cost: float = Field(..., example=150.0)
    selling_price: float = Field(..., example=240.0)
    criticality: int = Field(..., example=2)
    primary_supplier_id: Optional[str] = Field(None, example="SUP_001")

    class Config:
        from_attributes = True


class WarehouseResponse(BaseModel):
    warehouse_id: str = Field(..., example="WH_01")
    name: str = Field(..., example="Central Bhiwandi Mega-Warehouse")
    location: str = Field(..., example="Mumbai (Bhiwandi), Maharashtra")
    latitude: float = Field(..., example=19.2967)
    longitude: float = Field(..., example=73.0628)
    capacity: float = Field(..., example=150000.0)
    current_utilization: float = Field(..., example=0.74)
    operating_cost: float = Field(..., example=3500.0)
    status: str = Field(..., example="ACTIVE")

    class Config:
        from_attributes = True


class RouteResponse(BaseModel):
    route_id: str = Field(..., example="RT_0001")
    origin: str = Field(..., example="SUP_001")
    destination: str = Field(..., example="WH_08")
    origin_type: str = Field(..., example="SUPPLIER")
    destination_type: str = Field(..., example="WAREHOUSE")
    distance: float = Field(..., example=120.5)
    transport_mode: str = Field(..., example="ROAD")
    transit_time: float = Field(..., example=0.5)
    transportation_cost: float = Field(..., example=25.0)
    capacity: float = Field(..., example=5000.0)
    risk_level: float = Field(..., example=0.04)
    status: str = Field(..., example="OPEN")

    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    inventory_id: int = Field(..., example=1)
    warehouse_id: str = Field(..., example="WH_01")
    product_id: str = Field(..., example="PROD_ITEM_001")
    current_stock: float = Field(..., example=420.0)
    reserved_stock: float = Field(..., example=45.0)
    reorder_point: float = Field(..., example=350.0)
    safety_stock: float = Field(..., example=100.0)
    average_daily_demand: float = Field(..., example=35.0)
    stockout_risk: float = Field(..., example=0.08)

    class Config:
        from_attributes = True


class DemandZoneResponse(BaseModel):
    zone_id: str = Field(..., example="ZONE_01")
    name: str = Field(..., example="Delhi NCR Urban Demand Zone")
    region: str = Field(..., example="North")
    latitude: float = Field(..., example=28.6139)
    longitude: float = Field(..., example=77.2090)
    product_id: Optional[str] = Field(None, example="PROD_ITEM_001")
    historical_demand: float = Field(..., example=4500.0)
    forecast_demand: float = Field(..., example=4850.0)
    demand_growth: float = Field(..., example=0.078)

    class Config:
        from_attributes = True


class NetworkSummaryResponse(BaseModel):
    total_nodes: int = Field(..., example=83)
    total_edges: int = Field(..., example=160)
    nodes_by_type: Dict[str, int] = Field(..., example={
        "SUPPLIER": 20, "PRODUCTION": 8, "WAREHOUSE": 10, "HUB": 15, "DEMAND_ZONE": 30
    })
    status: str = Field(..., example="OPERATIONAL")


# -------------------------------------------------------------
# ML & Analytics Schemas
# -------------------------------------------------------------

class ForecastRequest(BaseModel):
    product_id: Optional[str] = Field("PROD_ITEM_001", description="Target SKU to forecast", example="PROD_ITEM_001")
    horizon_weeks: int = Field(8, ge=1, le=52, description="Forecast horizon in weeks", example=8)


class ForecastResponse(BaseModel):
    product_id: str
    model_name: str
    horizon_weeks: int
    forecasted_demand: List[float]
    metrics_benchmarks: Dict[str, Any]
    generated_at: str


class RiskPredictRequest(BaseModel):
    on_time_rate: float = Field(0.88, ge=0.0, le=1.0, example=0.88)
    average_delay: float = Field(3.5, ge=0.0, example=3.5)
    delay_frequency: float = Field(0.12, ge=0.0, le=1.0, example=0.12)
    quality_score: float = Field(0.92, ge=0.0, le=1.0, example=0.92)
    lead_time: float = Field(5.0, ge=0.5, example=5.0)
    lead_time_variability: float = Field(1.5, ge=0.0, example=1.5)
    capacity_utilization: float = Field(0.92, ge=0.0, le=1.0, example=0.92)
    historical_delays: int = Field(8, ge=0, example=8)


class RiskPredictResponse(BaseModel):
    disruption_probability: float = Field(..., example=0.742)
    is_high_risk: bool = Field(..., example=True)
    risk_tier: str = Field(..., example="CRITICAL")
    risk_drivers: List[str] = Field(..., example=["Low on-time delivery reliability", "Near-capacity strain (>90% utilization)"])


class AnomalyDetectRequest(BaseModel):
    events: List[Dict[str, Any]] = Field(..., example=[
        {"order_id": "ORD_TEST_1", "quantity": 120.0, "is_late": 1, "lead_time_deviation": 4.5},
        {"order_id": "ORD_TEST_2", "quantity": 25.0, "is_late": 0, "lead_time_deviation": 0.0}
    ])


class AnomalyDetectResponse(BaseModel):
    total_events_scanned: int
    anomalies_detected_count: int
    anomalies: List[Dict[str, Any]]


# -------------------------------------------------------------
# Impact & Simulation Schemas
# -------------------------------------------------------------

class ImpactAnalyzeRequest(BaseModel):
    entity_type: str = Field("SUPPLIER", example="SUPPLIER")  # SUPPLIER, WAREHOUSE, ROUTE
    entity_id: str = Field("SUP_001", example="SUP_001")
    capacity_reduction: float = Field(0.80, ge=0.0, le=1.0, example=0.80)
    duration_days: int = Field(10, ge=1, le=60, example=10)


class ImpactAnalyzeResponse(BaseModel):
    disrupted_entity: Dict[str, Any]
    dependent_products_count: Optional[int] = 0
    dependent_products: Optional[List[str]] = []
    affected_warehouses_count: Optional[int] = 0
    warehouse_runway_analysis: Optional[List[Dict[str, Any]]] = []
    affected_demand_zones: Optional[List[str]] = []
    estimated_shortage_units: Optional[float] = 0.0
    baseline_service_level: Optional[float] = 0.98
    projected_service_level: Optional[float] = 0.82
    service_level_deficit: Optional[float] = 0.16
    alternative_suppliers: Optional[List[Dict[str, Any]]] = []


class ScenarioSimulateRequest(BaseModel):
    scenario_type: str = Field("SUPPLIER_FAILURE", example="SUPPLIER_FAILURE")
    parameters: Dict[str, Any] = Field(..., example={
        "supplier_id": "SUP_001",
        "capacity_reduction": 0.80,
        "duration_days": 10
    })


class ScenarioSimulateResponse(BaseModel):
    scenario_type: str
    parameters: Dict[str, Any]
    applied_disruptions: List[Dict[str, Any]]
    simulated_network_state: Dict[str, Any]


# -------------------------------------------------------------
# Optimization & Recommendation Schemas
# -------------------------------------------------------------

class OptimizeRequest(BaseModel):
    scenario_type: str = Field("SUPPLIER_FAILURE", example="SUPPLIER_FAILURE")
    parameters: Dict[str, Any] = Field(default_factory=dict, example={
        "supplier_id": "SUP_001",
        "capacity_reduction": 0.80,
        "duration_days": 10
    })
    risk_aversion_weight: float = Field(50.0, example=50.0)


class OptimizeResponse(BaseModel):
    baseline: Dict[str, Any]
    nexus_optimized: Dict[str, Any]
    impact_comparison: Dict[str, Any]
    recommendation: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    recommendation_id: str
    run_id: str
    title: str
    reason: str
    affected_entities: Dict[str, Any]
    action_type: str
    expected_benefit: str
    expected_cost: float
    confidence_score: float
    created_at: str

    class Config:
        from_attributes = True
