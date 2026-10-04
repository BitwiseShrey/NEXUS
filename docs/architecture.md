# NEXUS System Architecture

## 1. Architectural Philosophy

NEXUS is engineered as a **general-purpose supply-chain decision-intelligence platform**. Rather than functioning merely as a descriptive dashboard or isolated machine learning predictor, NEXUS integrates the entire loop of supply chain management:

$$\text{Monitor} \longrightarrow \text{Predict} \longrightarrow \text{Analyze Impact} \longrightarrow \text{Simulate} \longrightarrow \text{Optimize} \longrightarrow \text{Recommend}$$

```
                           DATA SOURCES
                                 │
           ┌─────────────────────┼─────────────────────┐
           ↓                     ↓                     ↓
     Public Datasets       Digital Twin         External Shocks
    (Walmart, DataCo)    (Indian Topology)    (Weather, Strikes)
           │                     │                     │
           └─────────────────────┼─────────────────────┘
                                 ↓
                     DATA INGESTION & PIPELINE
              (Validation, Cleaning, Normalization)
                                 ↓
                    RELATIONAL DATABASE ENGINE
              (PostgreSQL / SQLite Standalone Fallback)
                                 ↓
                DIGITAL SUPPLY CHAIN TWIN (NetworkX)
            (83 Nodes: Suppliers, Plants, WHs, Hubs, Zones)
                                 ↓
           ┌─────────────────────┼─────────────────────┐
           ↓                     ↓                     ↓
    DEMAND FORECASTING    SUPPLIER RISK ENGINE    GIS & TOPOLOGY
    (XGBoost vs Baselines) (Supervised Classifier) (Haversine/Tortuosity)
           │                     │                     │
           └─────────────────────┼─────────────────────┘
                                 ↓
                     DISRUPTION IMPACT ENGINE
                     (Graph Failure Propagation)
                                 ↓
                     SCENARIO SIMULATION ENGINE
                   (Non-destructive State Clones)
                                 ↓
                     OPTIMIZATION ENGINE (OR-Tools)
                   (Multi-Echelon Mixed-Integer LP)
                                 ↓
                    ACTIONABLE RECOMMENDATIONS
                  (Plain-Language Business Advice)
                                 ↓
                    FASTAPI RESTful BACKEND
                     (OpenAPI 3.1 / Swagger)
```

---

## 2. Component Subsystems

### 2.1 Data Ingestion & Preprocessing Layer (`pipeline/`)
- **Ingestion**: Ingests raw empirical time-series data (Walmart Store Sales: 421,570 records) and delivery performance logs (DataCo Global Logistics: 35,000 records).
- **Validation**: Strict schema checks, negative sales filtering, lead-time variance calculation, and entity target verification ($N_{\text{suppliers}} \ge 20$, $N_{\text{orders}} \ge 50,000$).
- **Storage**: Clean Parquet data structures and relational tables.

### 2.2 Relational Database Layer (`backend/app/database.py`, `backend/app/models/`)
- Implemented with **SQLAlchemy 2.0 ORM**.
- Defaulting to PostgreSQL in production environments with seamless SQLite fallback for zero-dependency standalone capstone evaluation.
- Relational schema encompasses 14 tables:
  1. `suppliers`
  2. `products`
  3. `production_units`
  4. `warehouses`
  5. `distribution_hubs`
  6. `inventory`
  7. `demand_zones`
  8. `routes`
  9. `orders`
  10. `disruptions`
  11. `risk_events`
  12. `forecasts`
  13. `optimization_runs`
  14. `recommendations`

### 2.3 Digital Supply Chain Twin & GIS (`digital_twin/`)
- Modeled over authentic Indian logistics corridors covering North, West, South, East, and Central India.
- Graph Engine built with **NetworkX** (`SupplyChainGraph`) modeling multi-tier directional dependencies:
  $$\text{Suppliers} \longrightarrow \text{Production Units} \longrightarrow \text{Central Warehouses} \longrightarrow \text{Regional Hubs} \longrightarrow \text{Demand Zones}$$
- Geospatial engine calculates Haversine great-circle distances and realistic highway route tortuosity (1.22x factor for Indian national highways), supporting radius disruption queries and GeoJSON mapping.

### 2.4 Machine Learning Layer (`ml/`)
- **Demand Forecasting**: Autoregressive lag features ($t-1, t-2, t-4, t-8$), rolling moving averages, calendar seasonality, and trend. Compares Naive persistence and Moving Average baselines against an XGBoost Regressor.
- **Supplier Risk Prediction**: Supervised binary classifier balancing class imbalance (`scale_pos_weight`) to predict high-risk suppliers before catastrophic delivery breaches occur.
- **Anomaly Detection**: Unsupervised `IsolationForest` detecting demand surges, transit delays, and order pattern anomalies.

### 2.5 Disruption Impact & Scenario Simulation Layer (`impact/`, `simulation/`)
- **Impact Propagation**: Graph traversal downstream to identify exposed products, dependent distribution centers, estimated inventory runways, and expected service-level collapse.
- **Scenario Simulation**: Uses in-memory state cloning (`SimulationState`) to model supplier failures, road blockades, demand spikes, and warehouse shutdowns without altering the base persistent database.

### 2.6 Optimization & Recommendation Layer (`optimization/`, `recommendation/`)
- **Google OR-Tools**: Formulates multi-echelon linear allocation minimizing procurement, freight, holding, shortage penalties, and risk penalties.
- **Baseline Comparison**: Empirically benchmarks the optimized solution against standard heuristic un-optimized operations, proving cost savings and service-level gains.
- **Recommendation Engine**: Converts mathematical decision variables into plain-language actionable advice with quantified benefits, persisted for executive review.

### 2.7 Application API Layer (`backend/app/`)
- Built with **FastAPI** and **Pydantic v2**.
- Structured REST endpoints, OpenAPI Swagger UI (`/docs`), robust error handling, CORS headers, and health telemetry.
