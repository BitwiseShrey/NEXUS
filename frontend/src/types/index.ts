// NEXUS Frontend TypeScript Types & Interfaces (strictly mirrored from FastAPI Pydantic models)

export interface Supplier {
  supplier_id: string;
  supplier_name: string;
  location: string;
  latitude: number;
  longitude: number;
  product_categories: string;
  capacity: number;
  lead_time: number;
  unit_cost: number;
  on_time_rate: number;
  quality_score: number;
  risk_score: number;
  status: 'ACTIVE' | 'DISRUPTED' | 'SUSPENDED' | string;
}

export interface Product {
  product_id: string;
  product_name: string;
  category: string;
  unit_cost: number;
  selling_price: number;
  criticality: number;
  primary_supplier_id?: string;
}

export interface Warehouse {
  warehouse_id: string;
  name: string;
  location: string;
  latitude: number;
  longitude: number;
  capacity: number;
  current_utilization: number;
  operating_cost: number;
  status: 'ACTIVE' | 'CONGESTED' | 'SHUTDOWN' | string;
}

export interface RouteItem {
  route_id: string;
  origin: string;
  destination: string;
  origin_type: string;
  destination_type: string;
  distance: number;
  transport_mode: 'ROAD' | 'RAIL' | 'AIR' | string;
  transit_time: number;
  transportation_cost: number;
  capacity: number;
  risk_level: number;
  status: 'OPEN' | 'CONGESTED' | 'BLOCKED' | string;
}

export interface InventoryItem {
  inventory_id: number;
  warehouse_id: string;
  product_id: string;
  current_stock: number;
  reserved_stock: number;
  reorder_point: number;
  safety_stock: number;
  average_daily_demand: number;
  stockout_risk: number;
}

export interface DemandZone {
  zone_id: string;
  name: string;
  region: 'North' | 'West' | 'South' | 'East' | 'Central' | string;
  latitude: number;
  longitude: number;
  product_id?: string;
  historical_demand: number;
  forecast_demand: number;
  demand_growth: number;
}

export interface NetworkSummary {
  total_nodes: number;
  total_edges: number;
  nodes_by_type: {
    SUPPLIER: number;
    PRODUCTION: number;
    WAREHOUSE: number;
    HUB: number;
    DEMAND_ZONE: number;
  };
  status: string;
}

export interface AnalyticsSummary {
  suppliers: {
    total_suppliers: number;
    mean_on_time_rate: number;
    min_on_time_rate: number;
    mean_quality_score: number;
    mean_lead_time_days: number;
    mean_risk_score: number;
    total_capacity_units: number;
    high_risk_suppliers_count: number;
  };
  inventory: {
    total_skus_tracked: number;
    total_inventory_valuation_inr: number;
    mean_stockout_risk: number;
    critical_stockout_skus: number;
    mean_stock_coverage_days: number;
    below_reorder_point_count: number;
  };
  routes: {
    total_routes: number;
    mean_distance_km: number;
    mean_transit_days: number;
    mean_cost_per_shipment: number;
    routes_by_mode: {
      ROAD?: number;
      RAIL?: number;
      AIR?: number;
      [key: string]: number | undefined;
    };
    mean_route_risk: number;
    open_routes_percentage: number;
  };
  fulfillment: {
    sample_orders_analyzed: number;
    on_time_delivery_rate: number;
    late_delivery_rate: number;
    mean_order_quantity: number;
    median_order_quantity: number;
  };
}

export interface GeoFacilityFeature {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number]; // [lon, lat]
  };
  properties: {
    id: string;
    name: string;
    type: "SUPPLIER" | "PRODUCTION" | "WAREHOUSE" | "HUB" | "DEMAND_ZONE";
    location: string;
    capacity?: number;
    risk_score?: number;
    utilization?: number;
    status?: string;
    region?: string;
    historical_demand?: number;
    forecast_demand?: number;
  };
}

export interface GeoFacilityCollection {
  type: "FeatureCollection";
  total_features: number;
  features: GeoFacilityFeature[];
}

export interface ForecastRequest {
  product_id?: string;
  horizon_weeks?: number;
}

export interface ForecastResponse {
  product_id: string;
  model_name: string;
  horizon_weeks: number;
  forecasted_demand: number[];
  metrics_benchmarks: {
    [modelName: string]: {
      MAE: number;
      RMSE: number;
      sMAPE_percent: number;
    };
  };
  generated_at: string;
}

export interface RiskPredictRequest {
  on_time_rate: number;
  average_delay: number;
  delay_frequency: number;
  quality_score: number;
  lead_time: number;
  lead_time_variability: number;
  capacity_utilization: number;
  historical_delays: number;
}

export interface RiskPredictResponse {
  disruption_probability: number;
  is_high_risk: boolean;
  risk_tier: 'CRITICAL' | 'HIGH' | 'NORMAL' | string;
  risk_drivers: string[];
}

export interface NetworkRiskProfile {
  composite_network_risk_score: number;
  risk_status: 'HIGH_RISK' | 'MODERATE_RISK' | 'LOW_RISK' | string;
  dimensions: {
    supplier_risk: number;
    inventory_risk: number;
    route_risk: number;
    warehouse_risk: number;
  };
  top_vulnerable_suppliers: Array<{
    supplier_id: string;
    name: string;
    risk_score: number;
    risk_level: string;
    drivers: string[];
  }>;
  top_congested_warehouses: Array<{
    warehouse_id: string;
    name: string;
    risk_score: number;
    utilization: number;
    drivers: string[];
  }>;
}

export interface AnomalyEvent {
  order_id: string;
  quantity: number;
  is_late: number;
  lead_time_deviation: number;
}

export interface AnomalyItem {
  entity: string;
  anomaly_type: string;
  severity: number;
  score: number;
  timestamp: string;
  details: {
    quantity: number;
    is_late: boolean;
    lead_time_deviation: number;
  };
}

export interface ImpactAnalyzeRequest {
  entity_type: 'SUPPLIER' | 'WAREHOUSE' | 'ROUTE';
  entity_id: string;
  capacity_reduction?: number;
  duration_days?: number;
}

export interface ImpactAnalyzeResponse {
  disrupted_entity: {
    id: string;
    name: string;
    type: string;
    location?: string;
    nominal_capacity?: number;
    capacity_reduction_rate?: number;
    duration_days?: number;
  };
  dependent_products_count: number;
  dependent_products: string[];
  criticality_breakdown: {
    high_criticality_skus: string[];
    medium_criticality_skus: string[];
    low_criticality_skus: string[];
  };
  affected_warehouses_count: number;
  warehouse_runway_analysis: Array<{
    warehouse_id: string;
    product_id: string;
    current_stock: number;
    daily_demand: number;
    stock_runway_days: number;
    stockout_expected: boolean;
  }>;
  affected_demand_zones: string[];
  estimated_shortage_units: number;
  baseline_service_level: number;
  projected_service_level: number;
  service_level_deficit: number;
  alternative_suppliers: Array<{
    supplier_id: string;
    name: string;
    location: string;
    available_capacity: number;
    unit_cost: number;
    on_time_rate: number;
    risk_score: number;
  }>;
}

export interface ScenarioSimulateRequest {
  scenario_type: 'SUPPLIER_FAILURE' | 'ROUTE_DISRUPTION' | 'DEMAND_SPIKE' | 'WAREHOUSE_SHUTDOWN' | 'COMBINED_DISRUPTION';
  parameters: Record<string, any>;
}

export interface ScenarioSimulateResponse {
  scenario_type: string;
  parameters: Record<string, any>;
  applied_disruptions: Array<Record<string, any>>;
  simulated_network_state: {
    total_demand_units: number;
    total_available_supplier_capacity: number;
    net_capacity_balance: number;
    severed_routes_count: number;
    compromised_suppliers_count: number;
  };
}

export interface OptimizeRequest {
  scenario_type: string;
  parameters: Record<string, any>;
  risk_aversion_weight?: number;
}

export interface OptimizeResponse {
  baseline: {
    mode: string;
    status: string;
    total_demand: number;
    total_fulfilled: number;
    total_shortages: number;
    service_level: number;
    procurement_cost: number;
    transportation_cost: number;
    penalty_cost: number;
    holding_cost: number;
    total_cost: number;
    risk_exposure: number;
  };
  nexus_optimized: {
    mode: string;
    status: string;
    runtime_seconds: number;
    total_cost: number;
    service_level: number;
    total_demand: number;
    total_fulfilled: number;
    total_shortages: number;
    procurement_cost: number;
    transportation_cost: number;
    penalty_cost: number;
    allocations_count: number;
    top_allocations: Array<{
      from: string;
      to: string;
      units: number;
      type: string;
    }>;
  };
  impact_comparison: {
    cost_saved_inr: number;
    cost_reduction_percent: number;
    shortage_reduction_units: number;
    service_level_improvement_percentage_points: number;
    is_nexus_superior: boolean;
  };
  recommendation?: RecommendationItem;
}

export interface RecommendationItem {
  recommendation_id: string;
  run_id?: string;
  title: string;
  reason: string;
  recommended_actions: string[];
  affected_entities: {
    primary_disrupted_entity?: string;
    dependent_products?: string[];
    affected_warehouses?: number;
    affected_demand_zones?: string[];
    [key: string]: any;
  };
  action_type: string;
  expected_benefit: string;
  expected_cost: number;
  cost_saved_inr?: number;
  confidence_score: number;
  created_at: string;
}

export interface SystemHealth {
  status: string;
  app_name: string;
  environment: string;
  database: string;
  models_loaded: {
    demand_forecaster: boolean;
    supplier_risk_model: boolean;
    anomaly_detector: boolean;
  };
  all_systems_operational: boolean;
}
