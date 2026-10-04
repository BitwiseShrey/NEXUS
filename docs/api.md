# NEXUS REST API Documentation

## 1. Overview & Base Configuration

The NEXUS backend exposes a comprehensive RESTful API built with **FastAPI** and **Pydantic v2**.

- **Base URL**: `http://localhost:8000`
- **API Version Prefix**: `/api/v1`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Technical Specification**: `http://localhost:8000/redoc`
- **Data Format**: `application/json`

---

## 2. API Endpoints Catalog

### 2.1 System Health
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Validates DB connectivity, model readiness, and server status |

**Sample Response (`GET /health`):**
```json
{
  "status": "ONLINE",
  "app_name": "NEXUS",
  "environment": "development",
  "database": "HEALTHY",
  "models_loaded": {
    "demand_forecaster": true,
    "supplier_risk_model": true,
    "anomaly_detector": true
  },
  "all_systems_operational": true
}
```

---

### 2.2 Digital Twin Network Entities
| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/suppliers` | `status`, `category`, `limit` | List 20 suppliers with risk scores and capacity |
| `GET` | `/api/v1/products` | `category`, `criticality`, `limit`| List 50 catalog products |
| `GET` | `/api/v1/warehouses` | `status`, `limit` | List 10 fulfillment warehouses and utilization |
| `GET` | `/api/v1/routes` | `origin`, `destination`, `mode`, `status`| List 160 multimodal transit corridors |
| `GET` | `/api/v1/inventory` | `warehouse_id`, `critical_only` | List 500 SKU warehouse stock levels and stockout risks |
| `GET` | `/api/v1/demand` | `region`, `limit` | List 30 regional consumer demand zones |
| `GET` | `/api/v1/network` | None | Topology node and edge counts |

---

### 2.3 Operational Analytics & GIS
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/summary` | Executive dashboard KPIs (suppliers, inventory valuation, routes) |
| `GET` | `/api/v1/analytics/gis/facilities` | GeoJSON FeatureCollection of all Indian facilities for map visualization |

---

### 2.4 Demand Forecasting
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/forecast` | Generate multi-horizon demand forecasts using XGBoost regressor |
| `GET` | `/api/v1/forecasts` | List historical forecast runs |

**Sample Request (`POST /api/v1/forecast`):**
```json
{
  "product_id": "PROD_ITEM_001",
  "horizon_weeks": 4
}
```

**Sample Response:**
```json
{
  "product_id": "PROD_ITEM_001",
  "model_name": "XGBoost_Regressor",
  "horizon_weeks": 4,
  "forecasted_demand": [14520.5, 14890.2, 15120.0, 14950.8],
  "metrics_benchmarks": {
    "XGBoost_Regressor": {"MAE": 68553.14, "RMSE": 96042.50, "sMAPE_percent": 4.35},
    "Naive": {"MAE": 110961.63, "RMSE": 136255.10, "sMAPE_percent": 7.20}
  },
  "generated_at": "2026-09-26T16:35:00Z"
}
```

---

### 2.5 Risk Prediction & Unified Assessment
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/risk/predict` | Predict supplier disruption probability using supervised XGBoost classifier |
| `GET` | `/api/v1/risks` | Comprehensive network risk breakdown (supplier, inventory, route, warehouse) |

**Sample Request (`POST /api/v1/risk/predict`):**
```json
{
  "on_time_rate": 0.82,
  "average_delay": 4.5,
  "delay_frequency": 0.18,
  "quality_score": 0.89,
  "lead_time": 6.0,
  "lead_time_variability": 2.1,
  "capacity_utilization": 0.95,
  "historical_delays": 11
}
```

**Sample Response:**
```json
{
  "disruption_probability": 0.892,
  "is_high_risk": true,
  "risk_tier": "CRITICAL",
  "risk_drivers": [
    "Low on-time delivery reliability",
    "Excessive lead-time volatility",
    "Near-capacity strain (>90% utilization)",
    "Frequent historical shipment delays"
  ]
}
```

---

### 2.6 Anomaly Detection
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/anomaly/detect` | Isolation Forest multi-variate event anomaly scan |

---

### 2.7 Disruption Impact Propagation
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/impact/analyze` | Graph-based failure propagation quantifying downstream exposed products, warehouses, and shortage |

**Sample Request (`POST /api/v1/impact/analyze`):**
```json
{
  "entity_type": "SUPPLIER",
  "entity_id": "SUP_001",
  "capacity_reduction": 0.80,
  "duration_days": 10
}
```

---

### 2.8 Scenario Simulation & Optimization
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/scenario/simulate` | Non-destructive in-memory simulation of operational shocks |
| `POST` | `/api/v1/optimize` | Solves multi-echelon OR-Tools model, compares with baseline, and generates advice |
| `GET` | `/api/v1/optimization-runs` | Historical optimization runs |
| `GET` | `/api/v1/recommendations` | Audit trail of actionable plain-language recommendations |

**Sample Request (`POST /api/v1/optimize`):**
```json
{
  "scenario_type": "SUPPLIER_FAILURE",
  "parameters": {
    "supplier_id": "SUP_001",
    "capacity_reduction": 0.80,
    "duration_days": 10
  },
  "risk_aversion_weight": 50.0
}
```

**Sample Response:**
```json
{
  "baseline": {
    "mode": "BASELINE_UNOPTIMIZED",
    "total_cost": 41833559.60,
    "service_level": 0.5124,
    "total_shortages": 74967.0
  },
  "nexus_optimized": {
    "mode": "NEXUS_ORTOOLS_OPTIMIZED",
    "status": "OPTIMAL",
    "total_cost": 19291240.54,
    "service_level": 1.0,
    "total_shortages": 0.0
  },
  "impact_comparison": {
    "cost_saved_inr": 22542319.06,
    "cost_reduction_percent": 53.89,
    "shortage_reduction_units": 74967.0,
    "service_level_improvement_percentage_points": 48.76,
    "is_nexus_superior": true
  },
  "recommendation": {
    "recommendation_id": "REC_67B4E1A0",
    "title": "Mitigation Strategy for Tata AutoComp Components Disruption",
    "recommended_actions": [
      "Shift 16.8% (25000 units) of demand to SUP_005",
      "Shift 8.7% (13000 units) of demand to SUP_009",
      "Shift 10.6% (15802 units) of demand to SUP_010"
    ]
  }
}
```
