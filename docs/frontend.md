# NEXUS — Phase 2: Frontend Architecture & User Interface Documentation

## 1. Overview & System Purpose

The **NEXUS Frontend** is an enterprise-grade control-room dashboard built for supply chain intelligence, predictive risk management, and multi-echelon optimization. It is implemented in **React 19**, **TypeScript**, **Vite**, **Tailwind CSS**, and communicates directly with the **NEXUS FastAPI REST Backend** (`http://127.0.0.1:8000`).

The frontend faithfully maps to the 6-stage core operational paradigm:

$$\mathbf{MONITOR} \longrightarrow \mathbf{PREDICT} \longrightarrow \mathbf{ANALYZE\ IMPACT} \longrightarrow \mathbf{SIMULATE} \longrightarrow \mathbf{OPTIMIZE} \longrightarrow \mathbf{RECOMMEND}$$

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Framework** | React + TypeScript | React 19, TS 6.0 | Component rendering, type safety, modular design |
| **Bundler / Tooling** | Vite | 8.3+ | Fast HMR, optimized production build |
| **Styling** | Tailwind CSS | 3.4.17 | Control-room dark aesthetic (`nexus-950` to `nexus-700`) |
| **Icons** | Lucide React | Latest | Unified minimalist iconography |
| **Server State & Cache**| TanStack React Query | v5 | Automated background caching, refetching, mutation states |
| **Data Visualization** | Recharts | 3.10+ | Responsive multi-series charts (actuals vs predicted, cost comparisons) |
| **GIS Mapping** | React Leaflet + Leaflet | Leaflet 1.9+ | Interactive Indian supply-chain topology, geodesic polyline corridors |
| **HTTP Client** | Axios | 1.20+ | Typed REST client with Vite reverse proxying (`/api` -> port 8000) |
| **Routing** | React Router DOM | v7 | Client-side SPAs with history support and deep linking |

---

## 3. Application Architecture & Directory Structure

```
frontend/
├── index.html                   # HTML entry point with title and fonts
├── package.json                 # Dependencies & build scripts
├── postcss.config.js            # PostCSS configuration
├── tailwind.config.js           # NEXUS custom dark-control palette
├── tsconfig.json                # Project TypeScript configuration
├── tsconfig.app.json            # Application compiler options
├── vite.config.ts               # Vite server, path aliases, proxy to port 8000
└── src/
    ├── main.tsx                 # React DOM mount, StrictMode, global styles
    ├── App.tsx                  # QueryClientProvider, BrowserRouter, AppLayout routing
    ├── index.css                # Tailwind directives & dark Leaflet map styling
    ├── api/
    │   ├── client.ts            # Configured Axios instance with baseURL & timeouts
    │   └── index.ts             # Typed API functions for all 16 FastAPI backend endpoints
    ├── types/
    │   └── index.ts             # Pydantic-mirrored TypeScript schemas (GeoJSON, Analytics, etc.)
    ├── utils/
    │   └── formatters.ts        # Currency (INR ₹), percentage, numbers, and badge styles
    ├── components/
    │   ├── common/
    │   │   ├── KpiCard.tsx          # Reusable control metric card with trend & glow
    │   │   ├── RiskBadge.tsx        # Color-coded risk status (LOW, MEDIUM, HIGH, CRITICAL)
    │   │   ├── StatusBadge.tsx      # Facility status badge (ACTIVE, CONGESTED, SEVERED)
    │   │   ├── WorkflowBreadcrumb.tsx # 6-stage lifecycle stepper with active route tracking
    │   │   └── FeedbackStates.tsx   # LoadingSkeleton, ErrorState, EmptyState
    │   └── layout/
    │       ├── Sidebar.tsx          # Collapsible navigation drawer with live backend status
    │       ├── Navbar.tsx           # Real-time backend health monitor & manual refresh trigger
    │       └── AppLayout.tsx        # Persistent shell with Navbar, Sidebar, and Breadcrumb
    └── pages/
        ├── ExecutiveOverview.tsx    # Route: / (KPI grid, charts, network health, anomalies)
        ├── DigitalTwinMap.tsx       # Route: /network (Interactive Leaflet map with 83 nodes & 160 routes)
        ├── DemandIntelligence.tsx   # Route: /forecast (XGBoost demand projections vs actuals)
        ├── RiskIntelligence.tsx     # Route: /risk (ML-predicted supplier risk roster & live scoring)
        ├── ImpactAnalysis.tsx       # Route: /impact (Graph propagation, 6-stage cascade & runway)
        ├── ScenarioSimulation.tsx   # Route: /simulation (Disruption builder & network stress test)
        ├── OptimizationEngine.tsx   # Route: /optimize (Google OR-Tools solver vs baseline comparison)
        └── RecommendationCenter.tsx # Route: /recommendations (Actionable mitigation directives & ERP dispatch)
```

---

## 4. Screen-by-Screen Functional Specifications

### Screen 1: Executive Overview (`/`)
- **Stage**: `MONITOR`
- **Endpoints Used**: `GET /api/v1/analytics/overview`, `GET /api/v1/anomalies/detect`, `GET /health`
- **Key Features**:
  - High-level KPI cards: On-time delivery SLA (%), Network inventory valuation (INR ₹), Vulnerable suppliers count, Stockout-risk SKUs.
  - Interactive multi-tab data visualization:
    - *Network Composition*: Bar chart break-down of 20 Suppliers, 8 Plants, 10 Warehouses, 15 Hubs, 30 Demand Zones.
    - *Fulfillment Performance*: Delivery status distribution (On-Time, Late, Critical Delay).
    - *Inventory by Echelon*: Total stock distribution across plants and central warehouses.
  - Real-time Isolation Forest Anomaly Radar: Displays flagged transactions, anomaly scores, and root-cause indicators.
  - Active disruptions feed and quick-launch links to downstream stages.

### Screen 2: Digital Twin GIS Network Map (`/network`)
- **Stage**: `MONITOR`
- **Endpoints Used**: `GET /api/v1/gis/network`, `GET /api/v1/analytics/overview`
- **Key Features**:
  - Full-screen dark-themed Leaflet map focused on the Indian subcontinent (`lat: 20.5937, lng: 78.9629`, zoom 5).
  - 83 Geocoded facilities rendered via dynamic SVG `L.divIcon` markers:
    - Suppliers (Amber, hexagonal icon)
    - Production Plants (Cyan, factory icon)
    - Warehouses (Blue, warehouse icon)
    - Regional Hubs (Purple, hub icon)
    - Demand Zones (Green, map-pin icon)
  - 160 Geodesic multi-echelon corridors rendered with colored polylines (Road, Rail, Air) with tooltips displaying tortuosity distance and transit hours.
  - Facility filter toggles (by type and status), route visibility toggles, and detail inspection drawer.

### Screen 3: Demand Intelligence & Forecasting (`/forecast`)
- **Stage**: `PREDICT`
- **Endpoints Used**: `GET /api/v1/entities/products`, `POST /api/v1/forecast/predict`
- **Key Features**:
  - Product SKU selector (50 auto-parts SKUs) and forecast horizon slider (1 to 12 weeks).
  - Responsive Recharts graph plotting:
    - Historical actual demand (Solid slate line)
    - Heuristic Moving Average Baseline (Dotted amber line)
    - XGBoost ML Projections (Bright blue line with shadow fill)
  - Statistical benchmark scorecard displaying MAE, RMSE, and sMAPE (%) comparisons showing XGBoost accuracy superiority over naive baseline.
  - Tabular breakdown of weekly projected unit demand and buffer stock recommendations.

### Screen 4: Supplier Risk Intelligence (`/risk`)
- **Stage**: `PREDICT`
- **Endpoints Used**: `GET /api/v1/risk/suppliers`, `POST /api/v1/risk/predict`
- **Key Features**:
  - 20-Vendor supplier roster table with on-time delivery rates, defect rates, single-source flags, and ML risk scores.
  - Filterable by risk tier: All, Low (<30%), Medium (30-65%), High (>65%).
  - Interactive What-If Risk Simulator: Adjust on-time rate, defect rate, and single-source dependency sliders to instantly trigger real-time inference via the trained supervised risk model.
  - Radar chart displaying the top 5 most vulnerable supply nodes.

### Screen 5: Graph-Based Impact Propagation (`/impact`)
- **Stage**: `ANALYZE IMPACT`
- **Endpoints Used**: `GET /api/v1/entities/suppliers`, `POST /api/v1/impact/propagate`
- **Key Features**:
  - Failure injector: Select any supplier or warehouse, specify capacity degradation (10% to 100%), and set disruption window (days).
  - 6-Stage visual cascade diagram: Disrupted Facility $\rightarrow$ Tier-1 Plants $\rightarrow$ Finished Goods SKUs $\rightarrow$ Warehouses $\rightarrow$ Logistics Hubs $\rightarrow$ Demand Zones.
  - Warehouse Stock Runway Table: Evaluates current inventory vs daily burn rate to predict exact day of stockout.
  - Quantified network impact metrics: Estimated shortage units, baseline service level vs projected degradation, and alternative supplier discovery.

### Screen 6: Scenario Stress-Testing & Simulation (`/simulation`)
- **Stage**: `SIMULATE`
- **Endpoints Used**: `POST /api/v1/simulation/simulate`
- **Key Features**:
  - 5 Empirical disruption scenario builders:
    - Supplier Failure (Capacity shock)
    - Route Disruption (Corridor severance or transit delay)
    - Demand Spike (Tier-1 metro surge, e.g. Diwali festive spike)
    - Warehouse Shutdown (Natural hazard or labor action)
    - Combined Disruption (Concurrent supplier strike + corridor blockade)
  - Non-destructive execution against in-memory digital twin clones.
  - Before-vs-After delta comparison: Net capacity balance, severed routes count, compromised nodes, and projected unfulfilled demand.

### Screen 7: Multi-Echelon Optimization Engine (`/optimize`)
- **Stage**: `OPTIMIZE`
- **Endpoints Used**: `POST /api/v1/optimization/solve`, `GET /api/v1/optimization/history`
- **Key Features**:
  - Mathematical solver configuration: Risk aversion weight parameter ($\lambda \in [0, 100]$).
  - Side-by-side solver card comparison:
    - **Unoptimized Heuristic Baseline**: Greedy local assignment, total operational cost, service level, shortage units.
    - **NEXUS OR-Tools (GLOP) Optimized**: Multi-echelon linear program, total cost, 100% service level preservation, zero stock starvation.
  - Executive Financial Impact Banner: Quantified INR (₹) savings, cost reduction percentage, and shortage mitigation.
  - Recharts cost breakdown comparison (Procurement, Transportation, Holding, and Shortage Penalties).
  - Multi-echelon reallocation flow table detailing optimal supplier-to-warehouse and warehouse-to-zone dispatches.

### Screen 8: Strategic Recommendation Center (`/recommendations`)
- **Stage**: `RECOMMEND`
- **Endpoints Used**: `GET /api/v1/recommendations`, `POST /api/v1/optimization/solve`
- **Key Features**:
  - High-level KPI counters: Total AI Directives, Mean Model Confidence (%), Dispatched Actions, and Total Reallocation Cost.
  - Search & filter toolbar: Filter by action type (`REALLOCATE_AND_REROUTE`, `BUFFER_INVENTORY`), keyword, or confidence tier.
  - Detailed recommendation mitigation cards:
    - Unique Recommendation ID and Optimization Run ID badges.
    - Executive Rationale & Root Cause: Plain-language explanation of capacity degradation and potential failure modes.
    - Strategic Objective & Quantified Benefit: INR cost reduction, shortage units avoided, service level preservation.
    - Supply Chain Nodes & SKUs impact summary pills.
    - Solution Economics: Direct allocation cost, Google OR-Tools solver audit verification, SLA time-to-execute.
    - Interactive "Approve & Dispatch Strategy" button to simulate ERP/WMS handoff.
    - "Export Audit Brief (JSON)" action for enterprise compliance and review.
  - On-Demand Strategy Synthesizer: Run live optimizations directly from the recommendation center to generate new directives.

---

## 5. Development & Production Build Instructions

### Running Locally (Development Mode)

1. Ensure the NEXUS FastAPI backend is running:
   ```bash
   uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
3. Install dependencies (if not already installed):
   ```bash
   npm.cmd install
   ```
4. Start the Vite development server:
   ```bash
   npm.cmd run dev
   ```
5. Open your browser to `http://localhost:5173`.

### Production Build & Preview

1. Compile TypeScript and build the optimized production bundle:
   ```bash
   npm.cmd run build
   ```
2. Preview the production build locally:
   ```bash
   npm.cmd run preview
   ```
   Output bundle is stored in `frontend/dist/`.

---

## 6. Verification & Quality Assurance

- **TypeScript Compilation**: `tsc -b` passes with zero type errors.
- **Production Asset Bundling**: Vite compiles all CSS and JS bundles cleanly.
- **API Contract Fidelity**: 100% of data rendered in the UI is backed by the live FastAPI backend via strongly-typed Pydantic/TypeScript interfaces.
- **Backend Test Suite**: All 29/29 pytest automated tests continue passing without regression.
