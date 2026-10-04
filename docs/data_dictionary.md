# NEXUS Data Dictionary

Comprehensive reference for all digital twin entities, operational tables, and predictive schema attributes.

---

## 1. Core Digital Twin Entities

### 1.1 `suppliers`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | String(50) | Primary Key | Unique supplier code (e.g., `SUP_001`) |
| `supplier_name` | String(100) | Not Null | Industrial vendor name |
| `location` | String(100) | Not Null | City and state of manufacturing hub |
| `latitude` | Float | Not Null | Geodesic latitude coordinate |
| `longitude` | Float | Not Null | Geodesic longitude coordinate |
| `product_categories` | String(255) | Not Null | Category domain (Automotive, Electronics, etc.) |
| `capacity` | Float | Not Null | Monthly production capacity (units) |
| `lead_time` | Float | Not Null | Average fulfillment lead-time (days) |
| `unit_cost` | Float | Not Null | Baseline procurement cost per unit (INR) |
| `on_time_rate` | Float | Default 0.95 | Empirical historical on-time delivery ratio $[0.0, 1.0]$ |
| `quality_score` | Float | Default 0.98 | QA inspection acceptance ratio $[0.0, 1.0]$ |
| `historical_delays`| Integer | Default 0 | Cumulative past late shipment events |
| `risk_score` | Float | Indexed | Model-computed vulnerability index $[0.0, 1.0]$ |
| `status` | String(20) | Default 'ACTIVE' | Operational state: `ACTIVE`, `DISRUPTED`, `SUSPENDED` |

### 1.2 `products`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | String(50) | Primary Key | Catalog SKU code (e.g., `PROD_ITEM_001`) |
| `product_name` | String(100) | Not Null | Commercial item name |
| `category` | String(50) | Indexed | Sector category (Automotive, FMCG, Pharma, etc.) |
| `unit_cost` | Float | Not Null | Manufacturing / procurement cost (INR) |
| `selling_price` | Float | Not Null | Wholesale realization price (INR) |
| `criticality` | Integer | Default 1 | Priority tier (1: Commodity, 2: Medium, 3: Critical) |
| `primary_supplier_id`| String(50)| Foreign Key (`suppliers.supplier_id`) | Default contracted supplier |

### 1.3 `production_units`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `production_id` | String(50) | Primary Key | Assembly plant code (e.g., `PROD_01`) |
| `name` | String(100) | Not Null | Facility designation |
| `location` | String(100) | Not Null | City and state |
| `latitude` | Float | Not Null | Geodesic latitude |
| `longitude` | Float | Not Null | Geodesic longitude |
| `capacity` | Float | Not Null | Maximum daily assembly throughput (units) |
| `operational_status`| String(20)| Default 'OPERATIONAL' | Status: `OPERATIONAL`, `RESTRICTED`, `OFFLINE` |

### 1.4 `warehouses`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `warehouse_id` | String(50) | Primary Key | Fulfillment facility code (e.g., `WH_01`) |
| `name` | String(100) | Not Null | Depot description |
| `location` | String(100) | Not Null | City and state |
| `latitude` | Float | Not Null | Geodesic latitude |
| `longitude` | Float | Not Null | Geodesic longitude |
| `capacity` | Float | Not Null | Maximum storage capacity (units) |
| `current_utilization`| Float | Default 0.0 | Occupancy percentage $[0.0, 1.0]$ |
| `operating_cost` | Float | Default 1000.0 | Daily facility holding/operating cost (INR) |
| `status` | String(20) | Default 'ACTIVE' | State: `ACTIVE`, `CONGESTED`, `SHUTDOWN` |

### 1.5 `distribution_hubs`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `hub_id` | String(50) | Primary Key | Regional sorting terminal code (e.g., `HUB_01`) |
| `name` | String(100) | Not Null | Facility name |
| `location` | String(100) | Not Null | City and state |
| `latitude` | Float | Not Null | Geodesic latitude |
| `longitude` | Float | Not Null | Geodesic longitude |
| `capacity` | Float | Not Null | Cross-dock sorting throughput (units/day) |
| `status` | String(20) | Default 'ACTIVE' | Operational status |

### 1.6 `inventory`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `inventory_id` | Integer | Primary Key (Auto) | Unique inventory line item index |
| `warehouse_id` | String(50) | Foreign Key (`warehouses`) | Facility storing SKU |
| `product_id` | String(50) | Foreign Key (`products`) | Stored product identifier |
| `current_stock` | Float | Default 0.0 | Physically on-hand available inventory |
| `reserved_stock`| Float | Default 0.0 | Units allocated to pending outbound dispatches |
| `reorder_point` | Float | Default 100.0 | Inventory threshold triggering replenishment |
| `safety_stock` | Float | Default 50.0 | Buffer reserve protecting against demand surges |
| `average_daily_demand`| Float | Default 20.0 | Mean daily consumption rate |
| `stockout_risk` | Float | Default 0.05 | Estimated stock depletion probability $[0.0, 1.0]$ |

### 1.7 `demand_zones`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `zone_id` | String(50) | Primary Key | Regional consumer center (e.g., `ZONE_01`) |
| `name` | String(100) | Not Null | Urban market designation |
| `region` | String(50) | Indexed | Macro-region: `North`, `West`, `South`, `East`, `Central` |
| `latitude` | Float | Not Null | Geodesic latitude |
| `longitude` | Float | Not Null | Geodesic longitude |
| `product_id` | String(50) | Foreign Key (`products`) | Primary consumer SKU |
| `historical_demand`| Float | Default 0.0 | Baseline monthly demand volume (units) |
| `forecast_demand` | Float | Default 0.0 | Forward projected demand volume (units) |
| `demand_growth` | Float | Default 0.05 | Annualized demand growth trend $[0.0, 0.20]$ |

### 1.8 `routes`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `route_id` | String(50) | Primary Key | Corridor identifier (e.g., `RT_0001`) |
| `origin` | String(100) | Indexed | Origin facility ID |
| `destination` | String(100) | Indexed | Destination facility ID |
| `origin_type` | String(30) | Not Null | Origin entity type (`SUPPLIER`, `WAREHOUSE`, `HUB`) |
| `destination_type`| String(30)| Not Null | Destination entity type (`WAREHOUSE`, `HUB`, `ZONE`) |
| `distance` | Float | Not Null | Estimated highway distance (km) |
| `transport_mode`| String(30)| Default 'ROAD' | Transit modality: `ROAD`, `RAIL`, `AIR` |
| `transit_time` | Float | Not Null | Commercial transit duration (days) |
| `transportation_cost`| Float | Not Null | Freight cost per unit-trip (INR) |
| `capacity` | Float | Not Null | Maximum daily cargo throughput capacity |
| `risk_level` | Float | Default 0.05 | Disruption probability index $[0.0, 1.0]$ |
| `status` | String(20) | Default 'OPEN' | Corridor condition: `OPEN`, `CONGESTED`, `BLOCKED` |

---

## 2. Operational & Disruption Tables

### 2.1 `orders`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | String(50) | Primary Key | Transaction code (e.g., `ORD_000001`) |
| `product_id` | String(50) | Foreign Key (`products`) | Ordered SKU |
| `source` | String(100) | Not Null | Dispatch origin |
| `destination` | String(100) | Not Null | Delivery recipient |
| `quantity` | Float | Not Null | Quantity dispatched |
| `order_date` | DateTime | Indexed | Placement timestamp |
| `expected_delivery`| DateTime| Not Null | Promised delivery SLA deadline |
| `actual_delivery` | DateTime| Nullable | Recorded delivery timestamp |
| `status` | String(30) | Default 'DELIVERED'| Delivery status: `DELIVERED`, `LATE`, `CANCELED` |

### 2.2 `disruptions`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `disruption_id` | String(50) | Primary Key | Incident tracking code (e.g., `DIS_0001`) |
| `type` | String(50) | Not Null | Incident type: `WEATHER_FLOOD`, `STRIKE`, `SUPPLIER_FAILURE` |
| `location` | String(100) | Not Null | Geographic location of event |
| `start_date` | DateTime | Not Null | Start timestamp |
| `end_date` | DateTime | Nullable | Resolution timestamp |
| `severity` | Float | Not Null | Severity intensity $[0.0, 1.0]$ |
| `affected_supplier`| String(50)| Foreign Key (`suppliers`) | Impacted supplier entity |
| `affected_warehouse`| String(50)| Foreign Key (`warehouses`) | Impacted warehouse facility |
| `affected_route` | String(50)| Foreign Key (`routes`) | Impacted highway corridor |

---

## 3. Decision Intelligence & Optimization Tables

### 3.1 `forecasts`
| Column | Type | Description |
| :--- | :--- | :--- |
| `forecast_id` | String(50) | Unique forecast job identifier |
| `product_id` | String(50) | Target SKU |
| `model_name` | String(50) | Model used (`XGBoost_Regressor`, `MovingAverage_4W`, `Naive`) |
| `horizon_days` | Integer | Prediction horizon (e.g., 56 days / 8 weeks) |
| `forecast_values`| JSON | Array of predicted demand values |
| `metrics` | JSON | Comparative evaluation metrics (MAE, RMSE, sMAPE) |
| `generated_at` | DateTime | Execution timestamp |

### 3.2 `optimization_runs`
| Column | Type | Description |
| :--- | :--- | :--- |
| `run_id` | String(50) | Unique optimization execution ID |
| `scenario_name`| String(100) | Shock scenario tested |
| `objective_type`| String(50) | Optimization objective (`MINIMIZE_TOTAL_COST`) |
| `status` | String(30) | OR-Tools status: `OPTIMAL`, `FEASIBLE`, `INFEASIBLE` |
| `total_cost` | Float | Objective function value (INR) |
| `service_level`| Float | Percentage of demand satisfied $[0.0, 1.0]$ |
| `shortages_total`| Float | Total unmet demand units |
| `procurement_cost`| Float | Total procurement expenditure |
| `transportation_cost`| Float | Total logistics freight expenditure |
| `runtime_seconds`| Float | Solver compute duration |

### 3.3 `recommendations`
| Column | Type | Description |
| :--- | :--- | :--- |
| `recommendation_id`| String(50) | Actionable advice record code |
| `run_id` | String(50) | Linked `optimization_runs.run_id` |
| `title` | String(200) | Executive summary headline |
| `reason` | Text | Root-cause failure analysis |
| `affected_entities`| JSON | Structured list of impacted nodes |
| `action_type` | String(50) | Strategy: `REALLOCATE_AND_REROUTE`, `BUFFER_STOCK` |
| `expected_benefit`| Text | Quantified savings and shortage reduction |
| `expected_cost` | Float | Estimated implementation budget |
| `confidence_score`| Float | Model certainty index $[0.0, 1.0]$ |
