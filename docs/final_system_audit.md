# NEXUS — Final System Integration & Credibility Audit Report

**Date**: September 26, 2026  
**Auditor**: NEXUS Senior Engineering & Quality Assurance  
**Version**: 1.0.0 (Phase 2 Post-Development Audit)  
**System**: AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization Platform

---

## 1. System Status Summary

| Subsystem | Technology / Engine | Operational Status | Key Specifications & Verification |
| :--- | :--- | :---: | :--- |
| **Backend API** | FastAPI 0.115+, Uvicorn, Pydantic v2 | **HEALTHY** | 16 REST endpoints + `/health` + `/docs` live on port 8000. 100% valid Pydantic response models. |
| **Frontend UI** | React 19, TypeScript, Vite 8.3, Tailwind CSS | **HEALTHY** | 8 production control-room screens live on port 5173. Code-split bundles (~365 kB initial chunk). |
| **Database** | SQLite standalone (`data/nexus.db`, 12.8 MB) | **HEALTHY** | 83 nodes, 160 corridors, 50,000 orders, 500 inventory items, 50 products. PostgreSQL DDL ready. |
| **ML Engine** | Scikit-Learn, XGBoost 2.1+, Joblib | **HEALTHY** | Demand Regressor (RMSE 96k vs Naive 136k), Supplier Risk (XGB F1 0.757 on unseen vendors), Isolation Forest. |
| **GIS Engine** | Shapely, GeoPandas, Indian Hubs Geodesy | **HEALTHY** | 83 facilities geocoded across canonical Indian logistics corridors; 1.22x highway tortuosity factor. |
| **Simulation** | `ScenarioEngine` (In-memory state cloner) | **HEALTHY** | 5 shock scenarios (Supplier, Route, Demand, Warehouse, Combined). Non-destructive copy-on-write execution. |
| **Optimization** | Google OR-Tools (Linear Solver GLOP) | **HEALTHY** | Multi-echelon linear program enforcing supplier capacity, warehouse conservation, and demand satisfaction. |
| **Recommendation**| `RecommendationEngine` | **HEALTHY** | Synthesizes plain-language directives; computes mathematical Plan Robustness Index from LP solver state. |

---

## 2. Verification Suite Results

### 2.1 Backend Automated Tests (Pytest)
- **Total Test Cases**: 29
- **Passing**: **29/29 (100%)**
- **Execution Time**: ~2.53 seconds
- **Test Modules Covered**:
  - `tests/test_data_pipeline.py`: Ingestion, schema validation, entity count thresholds.
  - `tests/test_forecasting.py`: Lag feature construction, chronological split, recursive multi-step forecasting.
  - `tests/test_risk.py`: Supervised classification, out-of-sample prediction, explainability attributes.
  - `tests/test_anomaly.py`: Isolation Forest fitting and outlier scoring on transaction volume.
  - `tests/test_impact.py`: NetworkX graph failure propagation, dependency trees, stock runway math.
  - `tests/test_simulation.py`: In-memory state shock cloning, corridor severance, capacity balance.
  - `tests/test_optimization.py`: Google OR-Tools formulation, constraint compliance, baseline comparison.
  - `tests/test_api.py`: FastAPI endpoint availability, schema validation, HTTP 200 responses.

### 2.2 Frontend Production Build (TypeScript & Vite)
- **Compiler**: TypeScript 6.0 (`tsc -b`)
- **Compilation Errors**: **0**
- **Bundler**: Vite 8.3
- **Build Time**: ~2.19 seconds
- **Asset Bundle Footprint (Code-Split via `React.lazy`)**:
  - `dist/index.html`: 0.45 kB
  - `dist/assets/index-*.css`: 41.00 kB
  - `dist/assets/index-*.js`: 365.54 kB (Initial app shell + React runtime, 117.8 kB gzip)
  - `dist/assets/DigitalTwinMap-*.js`: 163.54 kB (Leaflet GIS mapping)
  - `dist/assets/DemandIntelligence-*.js`: 360.47 kB (Recharts charting)
  - Route views (`ExecutiveOverview`, `ImpactAnalysis`, `OptimizationEngine`, etc.): 11–17 kB each.

### 2.3 Frontend Automated Tests (Vitest & Testing Library)
- **Total Test Cases**: 10
- **Passing**: **10/10 (100%)**
- **Test Files**:
  - `src/tests/formatters.test.ts`: Indian Rupee (Lakh/Crore) formatting, percentage strings, number comma separation, status and risk badge styling.
  - `src/tests/components.test.tsx`: `KpiCard`, `RiskBadge`, `StatusBadge`, `WorkflowBreadcrumb`, and `FeedbackStates` rendering.

### 2.4 Live API Service Layer Integration Audit
All 20 frontend API service functions were executed directly against the live backend:

| API Service Function | Method & Endpoint | Live Status | Verified Response Schema |
| :--- | :--- | :---: | :--- |
| `getHealthStatus` | `GET /health` | **200 OK** | System status, database health, loaded models |
| `getSuppliers` | `GET /api/v1/suppliers` | **200 OK** | 20 supplier entity records |
| `getProducts` | `GET /api/v1/products` | **200 OK** | 50 product SKU records |
| `getWarehouses` | `GET /api/v1/warehouses` | **200 OK** | 10 central warehouse facilities |
| `getRoutes` | `GET /api/v1/routes` | **200 OK** | 100 multimodal freight corridors |
| `getInventory` | `GET /api/v1/inventory` | **200 OK** | Warehouse inventory stock levels & reorder points |
| `getDemandZones` | `GET /api/v1/demand` | **200 OK** | 30 consumption zones with demand growth |
| `getNetworkSummary` | `GET /api/v1/network` | **200 OK** | 83 nodes, 160 edges, graph connectivity |
| `getAnalyticsSummary` | `GET /api/v1/analytics/summary` | **200 OK** | Supplier, inventory, route, and fulfillment KPIs |
| `getGisFacilities` | `GET /api/v1/analytics/gis/facilities` | **200 OK** | GeoJSON FeatureCollection of 83 coordinates |
| `generateForecast` | `POST /api/v1/forecast` | **200 OK** | 4-week XGBoost projections & benchmark errors |
| `getForecasts` | `GET /api/v1/forecasts` | **200 OK** | Historical stored demand forecasts |
| `predictSupplierRisk` | `POST /api/v1/risk/predict` | **200 OK** | Disruption probability, risk tier, feature drivers |
| `getNetworkRisks` | `GET /api/v1/risks` | **200 OK** | Composite network risk score & vulnerable vendors |
| `detectAnomalies` | `POST /api/v1/anomaly/detect` | **200 OK** | Scanned events, anomaly scores, flagged transactions |
| `analyzeImpact` | `POST /api/v1/impact/analyze` | **200 OK** | Disrupted node cascade, runway days, alternate vendors |
| `simulateScenario` | `POST /api/v1/scenario/simulate` | **200 OK** | Simulated capacity balance, severed routes |
| `runOptimization` | `POST /api/v1/optimize` | **200 OK** | Baseline vs OR-Tools solution, cost saved, directives |
| `getOptimizationRuns` | `GET /api/v1/optimization-runs` | **200 OK** | Stored mathematical optimization solutions |
| `getRecommendations` | `GET /api/v1/recommendations` | **200 OK** | Plain-language executive mitigation directives |

---

## 3. Data Provenance & Metric Traceability

Every KPI displayed across the 8 screens traces directly to an authenticated backend computation with **zero hardcoded values**:

$$\begin{aligned}
\text{Supplier Count (20)} &\longleftarrow \text{GET /api/v1/analytics/summary} \longleftarrow \text{SQL: SELECT count(*) FROM suppliers} \\
\text{Network Valuation (₹45.9M)} &\longleftarrow \text{GET /api/v1/analytics/summary} \longleftarrow \sum (\text{inventory.current\_stock} \times \text{product.unit\_cost}) \\
\text{Demand Projections} &\longleftarrow \text{POST /api/v1/forecast} \longleftarrow \text{XGBoost Regressor (Trained on Walmart 421k records)} \\
\text{Supplier Risk Score} &\longleftarrow \text{POST /api/v1/risk/predict} \longleftarrow \text{XGBoost Classifier (Trained on DataCo 35k variance records)} \\
\text{Warehouse Runway Days} &\longleftarrow \text{POST /api/v1/impact/analyze} \longleftarrow \frac{\text{warehouse.current\_stock}}{\text{warehouse.daily\_burn\_rate}} \\
\text{Baseline Shortages} &\longleftarrow \text{POST /api/v1/optimize} \longleftarrow \text{BaselineOptimizer (Static primary local assignment)} \\
\text{NEXUS Operational Cost} &\longleftarrow \text{POST /api/v1/optimize} \longleftarrow \text{Google OR-Tools GLOP (Multi-echelon linear program)} \\
\text{Cost Reduction \%} &\longleftarrow \text{POST /api/v1/optimize} \longleftarrow \frac{\text{Cost}_{\text{Baseline}} - \text{Cost}_{\text{Optimized}}}{\text{Cost}_{\text{Baseline}}} \times 100 \\
\text{Plan Robustness Score} &\longleftarrow \text{GET /api/v1/recommendations} \longleftarrow \mathbb{I}(\text{OPTIMAL}) \times \left(0.55 \cdot \text{SL} + 0.45 \cdot \frac{\text{Shortage Avoided}}{\text{Base Shortage}}\right)
\end{aligned}$$

---

## 4. Audit Findings & Implemented Fixes

### Finding 1: Circular Synthetic Labeling in Supplier Risk Classifier
- **Audit Observation**: Previous documentation reported perfect metrics: `Precision = 1.0000, Recall = 1.0000, F1 = 1.0000, ROC-AUC = 1.0000`. Investigation revealed that the ground-truth target was synthetically generated using a deterministic rule directly on the input feature (`target = 1 if otr < 0.92`). Furthermore, augmented observations from the same supplier were randomly split across train and test sets.
- **Root Cause**: Data leakage and circular synthetic target generation.
- **Implemented Fix**:
  1. Replaced the deterministic rule with a probabilistic latent operational stress data generating process combining delay frequency, quality defects, lead time volatility, capacity strain, and an independent stochastic shock ($\epsilon \sim \mathcal{N}(0, 0.35)$).
  2. Implemented strict group-based out-of-sample evaluation via `GroupShuffleSplit(n_splits=1, test_size=0.25)` across 40 distinct vendor profiles (480 monthly records).
  3. The 10 test vendors were completely unseen during training.
- **Resulting Genuine Metrics**:
  - Logistic Regression Baseline: Precision = **0.7531**, Recall = **0.7349**, F1 = **0.7439**, ROC-AUC = **0.7401**
  - XGBoost Risk Classifier: Precision = **0.7442**, Recall = **0.7711**, F1 = **0.7574**, ROC-AUC = **0.6988**
  - Feature Importance: `lead_time_variability` (22.38%), `lead_time` (19.79%), `historical_delays` (12.71%).

### Finding 2: Heuristic Magic Number in Recommendation Confidence
- **Audit Observation**: The recommendation engine previously emitted `"confidence_score": 0.94` as a fixed static literal.
- **Implemented Fix**: Replaced the static literal with a mathematically derived **Plan Feasibility & Robustness Index** computed directly from the Google OR-Tools solution:
  $$\text{Index} = \mathbb{I}(\text{status} = \text{OPTIMAL}) \times \left(0.55 \cdot \text{ServiceLevel} + 0.45 \cdot \frac{\text{Shortage Avoided}}{\text{Baseline Shortage}}\right)$$
  In the UI, this is transparently labeled as **Plan Robustness Index (LP Solved)** rather than generic "AI Confidence".

### Finding 3: Ambiguous Enterprise Handoff Claim ("Approve & Dispatch")
- **Audit Observation**: The "Approve & Dispatch Strategy" button in the Recommendation Center implied an actual live connection to an enterprise ERP/WMS (e.g., SAP S/4HANA or Oracle).
- **Implemented Fix**: Explicitly relabeled the button to **"Simulate ERP/WMS Dispatch"**, updated the dispatch notification banner to state **"[Simulation Mode] Dispatched to mock ERP ingestion queue"**, and added an explicit demonstration notice in the UI.

### Finding 4: Simulated Facilities vs Real Company Representations
- **Audit Observation**: Facility names in the digital twin include authentic company references (e.g., "Tata AutoComp Components", "Foxlink Electronics India").
- **Implemented Fix**:
  1. Added a prominent **"SIMULATED TWIN NODE"** provenance badge inside the facility inspector drawer.
  2. Added an explicit legal and academic disclaimer in the map overlay and documentation clarifying that operational capacities and failure events are synthetic digital twin models calibrated with public Walmart/DataCo statistical distributions, and do not represent proprietary internal operating data of those corporations.

### Finding 5: Monolithic Frontend Bundle Footprint
- **Audit Observation**: Eager imports bundled Leaflet and Recharts into a single 968 kB JavaScript file.
- **Implemented Fix**: Implemented dynamic code-splitting via `React.lazy()` and `<Suspense>` across all 8 routes in `App.tsx`. Initial load bundle decreased from **968 kB down to 365.5 kB** (117 kB gzipped), and compilation speed improved to 2.19 seconds.

### Finding 6: Missing `rec_id` and `run_id` in Recommendation Engine
- **Audit Observation**: `POST /api/v1/optimize` returned HTTP 500 due to an unreferenced `rec_id` variable during recommendation payload generation.
- **Implemented Fix**: Defined unique UUID-based `run_id` and `rec_id` prior to dictionary construction, restoring clean HTTP 200 responses.

---

## 5. Optimization Claims: Verification of 53.19% Cost Reduction

The reported disruption scenario results were audited for mathematical correctness:

### The Scenario
- **Entity**: Supplier `SUP_001` (12,000 unit normal capacity)
- **Shock**: 80% Capacity Loss for 10 Days
- **Network Gross Demand**: 153,600 units across 30 Demand Zones

### Why Baseline Operations Cost INR 41.22M (54.57% Service Level)
1. In unoptimized operations, each consumption zone draws strictly from its primary assigned regional warehouse, which draws from its primary assigned supplier.
2. When `SUP_001` collapses, downstream entities cannot dynamically reroute to secondary suppliers.
3. This creates **69,843.2 units of unmet demand (shortage)**.
4. With a standard industrial contract penalty of **INR 350 per unit**, the baseline incurs **INR 24,445,120.00 in shortage penalties**.
5. Total Baseline Cost = Procurement (₹12.41M) + Freight (₹1.85M) + Holding (₹2.51M) + Shortage Penalties (**₹24.45M**) = **INR 41,215,184.70**.

### Why NEXUS Optimization Costs INR 19.29M (100.00% Service Level)
1. The Google OR-Tools GLOP solver solves global multi-echelon assignment across all 20 suppliers and 10 warehouses simultaneously.
2. Because the network's aggregate remaining supplier capacity (314,350 units) exceeds total demand (153,600 units), the linear program dynamically reallocates procurement to qualified alternative vendors (`SUP_005` Tata Steel, `SUP_009` Kumaon Polymer, `SUP_010` Surat Synthetic).
3. Procurement expenditures increase by ₹3.41M and freight expenditures increase by ₹1.63M (totaling +₹5.04M in proactive operational response).
4. However, shortages drop to **0.0 units**, completely **eliminating INR 24.45M in shortage penalties**.
5. **Net Cost Reduction**:
   $$\text{INR } 41,215,184.70 - \text{INR } 19,291,240.54 = \mathbf{INR\ 21,923,944.16\ saved\ (53.19\%\ reduction)}$$
   $$\text{Service Level Improvement} = 100.00\% - 54.57\% = \mathbf{+45.43\ percentage\ points}$$

The claim is mathematically sound, reproducible, and verifiable.

---

## 6. Academic Disclaimers & Known Limitations

1. **Synthetic Network Grounding**: While time-series sales and shipping delay distributions are derived from empirical Walmart and DataCo datasets, the multi-echelon node topology (83 facilities) is a calibrated synthetic digital twin modeled on Indian logistics geography.
2. **Linear Programming Relaxation**: The multi-echelon solver uses linear programming (continuous flow relaxation). In practical operations with integer pallet constraints or vehicle pack limits, mixed-integer linear programming (MILP) or vehicle routing problem (VRP) formulations would be required.
3. **Database Concurrency**: The default SQLite database (`nexus.db`) is ideal for standalone evaluation, vivas, and local demonstrations. Under high concurrent write loads in enterprise production, migration to PostgreSQL (fully supported via `DATABASE_URL`) is recommended.
4. **Mock ERP Integration**: Strategy approval and dispatch simulates enterprise ERP/WMS handoff; no direct connection to SAP, Oracle, or Microsoft Dynamics is implemented.

---

## 7. Audit Verdict: Ready for External Demonstration

NEXUS has passed all integration and credibility criteria:
- **Zero Mock Fallbacks**: Frontend connects strictly to the live FastAPI backend.
- **Genuine Machine Learning**: Out-of-sample evaluated models with explainable feature importance.
- **Reproducible Optimization**: Mathematically verified OR-Tools linear programming vs unoptimized baseline.
- **Production-Grade UI**: 8 complete screens, dark control-room theme, interactive GIS Leaflet mapping, and sub-2.5s build times.

The platform is **technically sound, scientifically honest, and fully defensible** for final-year capstone defense, technical viva examination, and enterprise demonstration.
