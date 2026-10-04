"""
NEXUS Report Generator - Part 3:
- Chapter 14: Multi-Echelon Mathematical Optimization Engine
- Chapter 15: Strategic Recommendation Engine
- Chapter 16: Flagship Demonstration Scenario: Tata AutoComp (SUP_001)
- Chapter 17: Backend API Architecture & REST Specification
- Chapter 18: Frontend Control Room Architecture
- Chapter 19: Screen-by-Screen Technical Documentation (All 8 Screens)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from scripts.doc_builder_helpers import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_callout,
    add_image_with_caption, add_custom_table, add_equation_block,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DARK_SLATE, COLOR_MUTED, COLOR_BODY
)


def build_chapter_14(doc):
    """Builds Chapter 14: Multi-Echelon Mathematical Optimization Engine."""
    add_heading_1(doc, "14. Multi-Echelon Mathematical Optimization Engine")

    add_heading_2(doc, "14.1 Linear Programming Model Formulation")
    add_paragraph(
        doc,
        "The core mathematical capability of NEXUS is its multi-echelon network flow optimization engine (`optimization/ortools_optimizer.py`). "
        "When an operational shock occurs, the optimizer formulates and solves a continuous **Linear Program (LP)** using Google OR-Tools. "
        "The model coordinates procurement, freight routing, warehouse handling, and shortage mitigation simultaneously across the entire network:"
    )

    add_paragraph(
        doc,
        "• Sets & Indices:\n"
        "  - $s \\in \\mathcal{S}$: Set of 20 suppliers\n"
        "  - $w \\in \\mathcal{W}$: Set of 10 fulfillment warehouses\n"
        "  - $d \\in \\mathcal{D}$: Set of 30 regional demand zones\n"
        "  - $\\mathcal{B} \\subset (\\mathcal{S} \\times \\mathcal{W}) \\cup (\\mathcal{W} \\times \\mathcal{D})$: Set of currently severed or blocked corridors\n\n"
        "• Parameters:\n"
        "  - $\\text{Cap}_s$: Available production capacity of supplier $s$ (units)\n"
        "  - $\\text{Cap}_w$: Storage and throughput capacity of warehouse $w$ (units)\n"
        "  - $\\text{Demand}_d$: Projected demand at consuming market zone $d$ (units)\n"
        "  - $c_s^{\\text{proc}}$: Procurement cost per unit from supplier $s$ (INR)\n"
        "  - $c_{s, w}^{\\text{trans}}$: Freight transport cost per unit from supplier $s$ to warehouse $w$ (default INR 15.0)\n"
        "  - $c_{w, d}^{\\text{trans}}$: Freight transport cost per unit from warehouse $w$ to demand zone $d$ (default INR 20.0)\n"
        "  - $c_w^{\\text{hold}}$: Handling and holding cost per unit at warehouse $w$ (default INR 8.0)\n"
        "  - $r_s$: Model-inferred risk score of supplier $s \\in [0, 1]$\n"
        "  - $\\lambda_{\\text{risk}}$: Risk aversion penalty coefficient (default 50.0)\n"
        "  - $p_{\\text{shortage}}$: Shortage penalty cost per unmet unit (default INR 350.0)\n\n"
        "• Decision Variables:\n"
        "  - $X_{s, w} \\ge 0$: Units procured from supplier $s$ and shipped to warehouse $w$\n"
        "  - $Y_{w, d} \\ge 0$: Units dispatched from warehouse $w$ to demand zone $d$\n"
        "  - $U_d \\ge 0$: Unmet shortage units at demand zone $d$"
    )

    add_heading_2(doc, "14.2 Objective Function & Cost Tradeoffs")
    add_paragraph(
        doc,
        "The objective function minimizes total operational cost across all echelons, balancing direct procurement and logistics against "
        "contractual shortage penalties and supplier vulnerability risk:"
    )

    add_equation_block(
        doc,
        "\\min \\mathcal{Z} = \\sum_{s \\in \\mathcal{S}} \\sum_{w \\in \\mathcal{W}} \\left(c_s^{\\text{proc}} + c_{s,w}^{\\text{trans}} + \\lambda_{\\text{risk}} \\cdot r_s\\right) X_{s, w} + \\sum_{w \\in \\mathcal{W}} \\sum_{d \\in \\mathcal{D}} \\left(c_w^{\\text{hold}} + c_{w,d}^{\\text{trans}}\\right) Y_{w, d} + \\sum_{d \\in \\mathcal{D}} p_{\\text{shortage}} \\cdot U_d",
        eq_num="Eq. 14.1",
        explanation="Multi-echelon objective function minimizing procurement, freight, holding, risk penalties, and shortage penalties."
    )

    add_heading_2(doc, "14.3 Mathematical Constraint Sets")
    add_paragraph(doc, "The solution space is governed by five linear constraint families enforced at runtime:")

    add_bullet(
        doc,
        "Total dispatches from any supplier cannot exceed that supplier's available physical capacity:\n"
        "$$\\sum_{w \\in \\mathcal{W}} X_{s, w} \\le \\text{Cap}_s \\quad \\forall s \\in \\mathcal{S}$$",
        bold_prefix="1. Supplier Capacity Constraints:"
    )
    add_bullet(
        doc,
        "Total inbound receipts at any warehouse cannot exceed its maximum storage throughput:\n"
        "$$\\sum_{s \\in \\mathcal{S}} X_{s, w} \\le \\text{Cap}_w \\quad \\forall w \\in \\mathcal{W}$$",
        bold_prefix="2. Warehouse Inbound Throughput Constraints:"
    )
    add_bullet(
        doc,
        "Outbound dispatches from a warehouse to demand zones cannot exceed total inbound units received:\n"
        "$$\\sum_{d \\in \\mathcal{D}} Y_{w, d} \\le \\sum_{s \\in \\mathcal{S}} X_{s, w} \\quad \\forall w \\in \\mathcal{W}$$",
        bold_prefix="3. Warehouse Flow Conservation Constraints:"
    )
    add_bullet(
        doc,
        "For every demand zone, total receipts from all warehouses plus unmet shortage must exactly satisfy projected demand:\n"
        "$$\\sum_{w \\in \\mathcal{W}} Y_{w, d} + U_d = \\text{Demand}_d \\quad \\forall d \\in \\mathcal{D}$$",
        bold_prefix="4. Demand Satisfaction & Shortage Balance Constraints:"
    )
    add_bullet(
        doc,
        "If a highway corridor is severed or a warehouse is shutdown, flow variables are clamped to zero:\n"
        "$$X_{s, w} = 0 \\quad \\forall (s, w) \\in \\mathcal{B}, \\qquad Y_{w, d} = 0 \\quad \\forall (w, d) \\in \\mathcal{B}$$",
        bold_prefix="5. Corridor Feasibility Constraints:"
    )

    add_heading_2(doc, "14.4 Google OR-Tools Solver Implementation")
    add_paragraph(
        doc,
        "NEXUS utilizes the **Google OR-Tools Linear Solver (`pywraplp.Solver.CreateSolver('GLOP')`)**. "
        "The problem comprises $20 \\times 10 + 10 \\times 30 + 30 = 530$ continuous variables and 70 constraints. "
        "GLOP solves this multi-echelon network problem in **0.006 to 0.016 seconds**, enabling interactive real-time optimization directly from the web browser."
    )

    add_heading_2(doc, "14.5 Baseline Heuristic Comparison Engine")
    add_paragraph(
        doc,
        "To quantify business value, NEXUS executes a parallel **Baseline Heuristic Optimizer** (`optimization/baseline_optimizer.py`). "
        "The baseline represents conventional enterprise behavior: rigid primary supplier allocations without agile cross-hub substitution. "
        "When a primary vendor suffers a capacity drop, the baseline incurs massive stockouts and SLA penalties, providing an authentic benchmark "
        "against which the mathematical optimization is evaluated."
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/15_cost_optimization_waterfall.png",
        "Figure 14.1 — Multi-Echelon Cost Breakdown: Baseline Heuristic vs. NEXUS OR-Tools Optimization",
        width=Inches(5.4)
    )

    doc.add_page_break()


def build_chapter_15(doc):
    """Builds Chapter 15: Strategic Recommendation Engine."""
    add_heading_1(doc, "15. Strategic Recommendation Engine")

    add_heading_2(doc, "15.1 Mathematical Translation of LP Solution Vectors")
    add_paragraph(
        doc,
        "Enterprise C-suite executives and operations directors do not make decisions by inspecting raw mathematical linear programming vectors. "
        "The NEXUS Recommendation Engine (`recommendation/recommendation_engine.py`) bridges the gap between operations research and executive management "
        "by translating numerical flow allocations into clear, actionable, plain-language directives."
    )
    add_paragraph(
        doc,
        "The engine extracts the top active allocations from the Google OR-Tools solution, computes the demand percentage shifts required, and "
        "synthesizes an executive mitigation brief detailing the root-cause failure, specific procurement shifts, warehouse buffer rebalances, and "
        "quantified financial savings in Indian Rupees (INR)."
    )

    add_heading_2(doc, "15.2 The Plan Feasibility & Robustness Index")
    add_paragraph(
        doc,
        "During the Phase 2 Credibility Audit, the recommendation engine was audited to eliminate arbitrary static literals. "
        "The static `'confidence_score': 0.94` was replaced with a formal mathematical metric derived directly from the linear solver state:",
        bold_prefix="The Robustness Index Formulation:"
    )

    add_equation_block(
        doc,
        "\\text{Plan Robustness Index} = \\mathbb{I}(\\text{status} = \\text{OPTIMAL}) \\times \\left(0.55 \\cdot \\text{ServiceLevel} + 0.45 \\cdot \\min\\left(1.0, \\max\\left(0.0, \\frac{\\text{Shortage Avoided}}{\\max(\\text{Base Shortage}, 1.0)}\\right)\\right)\\right)",
        eq_num="Eq. 15.1",
        explanation="Mathematical Plan Robustness Index where status is indicator of solver optimality, ServiceLevel is fraction of demand satisfied [0, 1], and Shortage Avoided is the units mitigated relative to baseline."
    )

    add_paragraph(
        doc,
        "The resulting index is clamped to $[0.50, 0.98]$ and displayed transparently in the UI as **Plan Robustness Index (LP Solved)**, "
        "providing mathematical proof that the mitigation strategy is both computationally optimal and operationally robust."
    )

    add_heading_2(doc, "15.3 Simulated ERP/WMS Dispatch Interface")
    add_paragraph(
        doc,
        "In the Strategic Recommendation Center (Screen 8), planners can review the mitigation strategy and click **'Simulate ERP/WMS Dispatch'**. "
        "In strict compliance with academic integrity guidelines, the UI transparently displays a **'[Simulation Mode]'** badge and dispatches the payload "
        "to a mock ERP ingestion queue, demonstrating how the system would interface with SAP or Oracle in an enterprise deployment."
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/08_recommendation_center.png",
        "Figure 15.1 — Strategic Recommendation Center (Screen 8: Actionable Directives, Plan Robustness Index 94%, and Simulated ERP Dispatch)",
        width=Inches(5.0)
    )

    doc.add_page_break()


def build_chapter_16(doc):
    """Builds Chapter 16: Flagship Demonstration Scenario: Tata AutoComp (SUP_001)."""
    add_heading_1(doc, "16. Flagship Demonstration Scenario: Tata AutoComp (SUP_001)")

    add_heading_2(doc, "16.1 Step-by-Step Scenario Execution Walkthrough")
    add_paragraph(
        doc,
        "To validate the end-to-end decision intelligence cycle, NEXUS executes a reproducible stress test on **Supplier SUP_001 "
        "(Tata AutoComp Components, Pune Chakan Hub)** (`docs/final_demo_scenario.md`):"
    )

    add_callout(
        doc,
        "DEMONSTRATED SCENARIO DISCLAIMER:\n"
        "This is a demonstrated simulated scenario designed to evaluate algorithm performance under controlled stress conditions. "
        "It does NOT represent the actual operational performance, factory capacities, or financial records of Tata AutoComp Components "
        "or Tata Steel. In this demonstrated simulated scenario, NEXUS reduced modeled operational cost by 53.89% versus the baseline heuristic.",
        alert_type="NOTE",
        title="SIMULATED SCENARIO DEMONSTRATION NOTICE"
    )

    add_paragraph(
        doc,
        "1. Initial Nominal State: The network operates 20 active suppliers, 500 SKUs, INR 45.92M inventory valuation, and an 83.0% on-time delivery SLA.\n"
        "2. Disruption Shock Injected: Supplier SUP_001 suffers an **80% capacity drop (12,000 -> 2,400 units/mo) for 10 days** due to simulated equipment boiler failure.\n"
        "3. Impact Propagation: NetworkX DiGraph traverses dependencies. Component PROD_ITEM_003 is compromised. Downstream warehouse WH_01 faces imminent stockout on Day 5 (Runway = 4.7 days). Five urban demand zones face severe component stockouts.\n"
        "4. In-Memory Simulation: State cloner generates an isolated sandbox. While total network demand is 153,600 units, the network retains 314,350 units of aggregate supplier capacity, proving that recovery is physically feasible if agile reallocation is executed.\n"
        "5. Mathematical Optimization: Google OR-Tools GLOP solves the 530-variable multi-echelon model in 0.0114 seconds, dynamically shifting component sourcing to secondary qualified vendors (SUP_005 Tata Steel Jamshedpur, SUP_009 Kumaon Polymer Pantnagar, SUP_010 Surat Synthetic)."
    )

    add_heading_2(doc, "16.2 Baseline vs. NEXUS Mathematical Comparison")
    
    demo_headers = ["Operational Performance Metric", "Baseline Heuristic Response", "NEXUS Optimized (Google OR-Tools)", "Differential Value-Add"]
    demo_data = [
        ["Total Operational Cost", "INR 41,833,559.60", "INR 19,291,240.54", "-53.89% (Saved INR 22,542,319.06)"],
        ["Procurement Cost", "INR 11,817,420.00", "INR 12,845,900.00", "+INR 1,028,480.00 (Agile substitution)"],
        ["Freight / Transportation", "INR 1,969,570.00", "INR 5,381,240.00", "+INR 3,411,670.00 (Cross-hub rerouting)"],
        ["Shortage Penalty Incurred", "INR 26,238,450.00", "INR 0.00", "-100% (INR 26.2M penalties eliminated)"],
        ["Holding Cost", "INR 1,808,119.60", "INR 1,064,100.54", "-INR 744,019.06 (Optimized inventory flow)"],
        ["Unmet Demand (Shortage)", "74,967.0 units", "0.0 units", "74,967 units saved (100% shortage avoided)"],
        ["Network Service Level", "51.24%", "100.00%", "+48.76 percentage points gain"],
        ["Solver Compute Time", "N/A (Static heuristic)", "0.0114 seconds", "Real-time decision response"]
    ]

    add_custom_table(
        doc,
        headers=demo_headers,
        data=demo_data,
        col_widths=[Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.7)],
        alignment=['L', 'R', 'R', 'C'],
        title="Table 16.1 — Flagship Scenario Benchmark: Baseline vs. NEXUS OR-Tools Performance"
    )

    add_heading_2(doc, "16.3 Anatomy of the 53.89% Cost Reduction")
    add_paragraph(
        doc,
        "A critical question during viva examination is: *'How does NEXUS achieve a 53.89% cost reduction?'*\n"
        "The mathematical explanation is straightforward and compelling:\n"
        "1. In the baseline heuristic, the loss of SUP_001 causes 74,967 units of unmet demand. Each unmet unit incurs a contractual SLA penalty of INR 350.00, "
        "exploding total shortage penalties to **INR 26,238,450.00**.\n"
        "2. The NEXUS optimizer dynamically invests an additional **INR 4.44M** in higher-cost secondary procurement (+INR 1.03M) and long-distance freight (+INR 3.41M).\n"
        "3. By spending INR 4.44M on rerouting, NEXUS completely eliminates INR 26.24M in stockout penalties.\n"
        "4. Net Financial ROI: INR 26.24M (penalties avoided) - INR 4.44M (rerouting costs) = **INR 22.54M Net Financial Savings (53.89% cost reduction)**."
    )

    doc.add_page_break()


def build_chapter_17(doc):
    """Builds Chapter 17: Backend API Architecture & REST Specification."""
    add_heading_1(doc, "17. Backend API Architecture & REST Specification")

    add_heading_2(doc, "17.1 FastAPI Framework & Pydantic v2 Contracts")
    add_paragraph(
        doc,
        "The NEXUS backend is architected as an enterprise RESTful API utilizing **FastAPI 0.115+** and **Pydantic v2**. "
        "FastAPI enforces strict schema validation on all incoming requests and outgoing responses, automatically generating OpenAPI 3.1 "
        "and JSON Schema specifications accessible via interactive Swagger UI (`/docs`) and ReDoc (`/redoc`)."
    )

    add_heading_2(doc, "17.2 Complete 20-Endpoint REST API Specification")
    
    api_headers = ["HTTP Method", "REST Endpoint URI", "Request Payload Schema", "Response Schema Contract", "Endpoint Description"]
    api_data = [
        ["GET", "/health", "None", "HealthResponse", "System readiness, DB connectivity, loaded ML models"],
        ["GET", "/api/v1/suppliers", "Query: limit, status", "List[SupplierSchema]", "List 20 suppliers with risk scores and capacity"],
        ["GET", "/api/v1/products", "Query: category, limit", "List[ProductSchema]", "List 50 catalog finished SKUs with unit costs"],
        ["GET", "/api/v1/warehouses", "Query: limit, status", "List[WarehouseSchema]", "List 10 fulfillment warehouses and utilization"],
        ["GET", "/api/v1/routes", "Query: origin, limit", "List[RouteSchema]", "List 160 multimodal transit freight corridors"],
        ["GET", "/api/v1/inventory", "Query: critical_only", "List[InventorySchema]", "List 500 SKU warehouse inventory stock levels"],
        ["GET", "/api/v1/demand", "Query: region, limit", "List[DemandZoneSchema]", "List 30 regional consumer demand consuming zones"],
        ["GET", "/api/v1/network", "None", "NetworkSummaryResponse", "Topology graph node and edge connectivity counts"],
        ["GET", "/api/v1/analytics/summary", "None", "AnalyticsSummaryResponse", "Executive dashboard operational KPIs"],
        ["GET", "/api/v1/analytics/gis/facilities", "None", "GeoJSONFeatureCollection", "GeoJSON FeatureCollection of 83 coordinates"],
        ["POST", "/api/v1/forecast", "ForecastRequest", "ForecastResponse", "XGBoost 4-week demand projection and benchmarks"],
        ["GET", "/api/v1/forecasts", "None", "List[ForecastRecord]", "List historical demand forecasting audit runs"],
        ["POST", "/api/v1/risk/predict", "SupplierRiskRequest", "SupplierRiskResponse", "Supervised XGBoost vendor disruption probability"],
        ["GET", "/api/v1/risks", "None", "NetworkRiskProfileResponse", "Unified multi-dimensional risk scores"],
        ["POST", "/api/v1/anomaly/detect", "None / Filter", "AnomalyDetectResponse", "Isolation Forest multi-variate event anomaly scan"],
        ["POST", "/api/v1/impact/analyze", "ImpactAnalyzeRequest", "ImpactAnalyzeResponse", "NetworkX cascading failure impact propagation"],
        ["POST", "/api/v1/scenario/simulate", "ScenarioSimulateRequest", "ScenarioSimulateResponse", "Non-destructive in-memory state shock cloning"],
        ["POST", "/api/v1/optimize", "OptimizeRequest", "OptimizeResponse", "Google OR-Tools multi-echelon optimization solve"],
        ["GET", "/api/v1/optimization-runs", "None", "List[OptimizationRunSchema]", "List historical OR-Tools optimization solutions"],
        ["GET", "/api/v1/recommendations", "None", "List[RecommendationResponse]", "Audit trail of plain-language executive directives"]
    ]

    add_custom_table(
        doc,
        headers=api_headers,
        data=api_data,
        col_widths=[Inches(0.9), Inches(1.7), Inches(1.2), Inches(1.3), Inches(1.4)],
        alignment=['C', 'L', 'L', 'L', 'L'],
        title="Table 17.1 — FastAPI RESTful API Endpoints Master Reference (20 Implemented Endpoints)"
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/09_swagger_api_docs.png",
        "Figure 17.1 — FastAPI Interactive OpenAPI 3.1 Swagger Documentation UI (Port 8000 /docs)",
        width=Inches(5.0)
    )

    doc.add_page_break()


def build_chapter_18(doc):
    """Builds Chapter 18: Frontend Control Room Architecture."""
    add_heading_1(doc, "18. Frontend Control Room Architecture")

    add_heading_2(doc, "18.1 React 19, TypeScript, and Vite 8.3")
    add_paragraph(
        doc,
        "The NEXUS frontend is architected as an enterprise-grade single-page application (SPA) utilizing **React 19.2.8**, **TypeScript 6.0**, "
        "and **Vite 8.3.1**. Styled with **Tailwind CSS 3.4**, the interface implements a bespoke 'control room' dark aesthetic designed for high-stress "
        "supply chain command centers."
    )

    add_heading_2(doc, "18.2 State Management with TanStack React Query")
    add_paragraph(
        doc,
        "Client-side asynchronous data synchronization is managed exclusively through **TanStack React Query v5** (`@tanstack/react-query`). "
        "Queries are configured with a 2-minute `staleTime` and background cache invalidation. Mutations (`useMutation`) manage optimization solves "
        "and scenario simulations, automatically triggering cache refetches upon successful completion without requiring full-page reloads."
    )

    add_heading_2(doc, "18.3 Code-Splitting, Lazy Loading & Bundle Footprint")
    add_paragraph(
        doc,
        "During the Phase 2 Credibility Audit, the frontend build was re-engineered to resolve monolithic bundle bloat. "
        "By implementing dynamic code-splitting via `React.lazy()` and `<Suspense>` across all 8 routes in `frontend/src/App.tsx`, the initial load "
        "bundle footprint was slashed by 62.2%:"
    )
    add_bullet(doc, "Pre-Audit Monolithic Bundle: 968.2 kB (Single un-split JavaScript chunk causing sluggish initial load)", bold_prefix="•")
    add_bullet(doc, "Post-Audit Initial App Shell: 365.54 kB (117.8 kB gzipped — fast initial load under 200 ms)", bold_prefix="•")
    add_bullet(doc, "Digital Twin Leaflet Route: 163.54 kB (Loaded on-demand only when visiting /network)", bold_prefix="•")
    add_bullet(doc, "Demand Intelligence Recharts Route: 360.47 kB (Loaded on-demand only when visiting /forecast)", bold_prefix="•")
    add_bullet(doc, "Individual Operations Views: 11 – 17 kB each (ExecutiveOverview, ImpactAnalysis, OptimizationEngine, etc.)", bold_prefix="•")

    doc.add_page_break()


def build_chapter_19(doc):
    """Builds Chapter 19: Screen-by-Screen Technical Documentation."""
    add_heading_1(doc, "19. Screen-by-Screen Technical Documentation")

    # 19.1 Executive Overview
    add_heading_2(doc, "19.1 Executive Overview Screen (Route: `/`)")
    add_paragraph(
        doc,
        "• Purpose: High-level command center providing instant operational visibility across the entire multi-echelon network.\n"
        "• User Problem: C-suite executives and supply chain directors need an immediate, unified view of network health without navigating complex menus.\n"
        "• UI Components: KPI Cards (On-Time Delivery SLA 83.0%, Inventory Valuation ₹4.59 Cr, Vulnerable Suppliers 3, Stockout Risk SKUs 0), "
        "Decision Intelligence Action Loop CTA buttons, Risk Dimensions progress bars, Critical Stockout Warnings table, and Network Vulnerability Badge (13.6/100 LOW_RISK).\n"
        "• Data Sources: `GET /api/v1/analytics/summary`, `GET /api/v1/risks`, `GET /api/v1/inventory?critical_only=true`.\n"
        "• Visualizations: Colored KPI metric badges, multi-dimensional risk progress bars, and inventory status chips."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/01_executive_overview.png",
        "Figure 19.1 — Screen 1: Executive Supply Chain Overview Dashboard",
        width=Inches(5.0)
    )

    # 19.2 Digital Twin Network Map
    add_heading_2(doc, "19.2 Digital Twin Network Map Screen (Route: `/network`)")
    add_paragraph(
        doc,
        "• Purpose: Interactive GIS visualization of the 83 Indian facilities and 160 transit corridors.\n"
        "• User Problem: Operations managers lack geographic visibility into where facilities are located and how transit corridors connect them.\n"
        "• UI Components: Full-screen Leaflet map, facility filter pills (All Nodes, Suppliers, Plants, Warehouses, Hubs, Demand Zones), "
        "color-coded node markers with pulsing glow, multimodal corridor lines, and slide-out Facility Inspector Drawer.\n"
        "• Data Sources: `GET /api/v1/analytics/gis/facilities` (GeoJSON FeatureCollection), `GET /api/v1/routes`.\n"
        "• User Interactions: Clicking any facility marker opens the inspector drawer showing throughput capacity, risk scores, and active status."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/02_digital_twin_network.png",
        "Figure 19.2 — Screen 2: Digital Supply Chain Twin Geospatial Network Map",
        width=Inches(5.0)
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/02b_digital_twin_facility_inspector.png",
        "Figure 19.3 — Screen 2b: Interactive Facility Inspector Drawer & Node Telemetry",
        width=Inches(5.0)
    )

    # 19.3 Demand Intelligence
    add_heading_2(doc, "19.3 Demand Intelligence & Forecasting Screen (Route: `/forecast`)")
    add_paragraph(
        doc,
        "• Purpose: Multi-horizon demand forecasting comparing XGBoost against statistical baselines.\n"
        "• User Problem: Planners struggle with stockouts and Bullwhip distortion caused by naive forecasting tools.\n"
        "• UI Components: SKU selector dropdown (50 products), forecast horizon selector (4, 8, 12 weeks), Benchmark Cards "
        "(XGBoost sMAPE 4.35%, Naive 7.20%, MA4 8.42%), and Recharts Area/Line chart plotting Historical vs. Baseline vs. NEXUS ML.\n"
        "• Data Sources: `POST /api/v1/forecast`, `GET /api/v1/products`, `GET /api/v1/demand`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/03_demand_intelligence.png",
        "Figure 19.4 — Screen 3: Demand Intelligence & Multi-Horizon Forecasting",
        width=Inches(5.0)
    )

    # 19.4 Risk Intelligence
    add_heading_2(doc, "19.4 Risk Intelligence Command Center (Route: `/risk`)")
    add_paragraph(
        doc,
        "• Purpose: Supervised supplier vulnerability prediction and multi-dimensional risk scoring.\n"
        "• User Problem: Procurement teams cannot anticipate which vendors are about to fail before deliveries breach SLAs.\n"
        "• UI Components: 20-Vendor Roster Table with risk badges, Vendor Inspector Drawer, and Live XGBoost Inference Sliders "
        "(allowing real-time manipulation of on-time rates, quality scores, and delays to observe instant ML disruption probability).\n"
        "• Data Sources: `GET /api/v1/suppliers`, `GET /api/v1/risks`, `POST /api/v1/risk/predict`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/04_risk_intelligence.png",
        "Figure 19.5 — Screen 4: Supply Chain Risk Command Center & Live ML Inference",
        width=Inches(5.0)
    )

    # 19.5 Impact Analysis
    add_heading_2(doc, "19.5 Disruption Impact Propagation Screen (Route: `/impact`)")
    add_paragraph(
        doc,
        "• Purpose: NetworkX graph-based failure cascading from disrupted nodes to downstream demand zones.\n"
        "• User Problem: When a supplier fails, planners cannot determine which warehouses will run out of stock and when.\n"
        "• UI Components: Disruption Shock Injector form (Entity type, ID, capacity cut slider, duration slider), 6-Stage Propagation "
        "Cascade Pipeline cards, Downstream Warehouse Stock Runways cards (e.g. WH_01 4.7 days runway), and Discovered Alternative Suppliers.\n"
        "• Data Sources: `POST /api/v1/impact/analyze`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/05_impact_analysis.png",
        "Figure 19.6 — Screen 5: Disruption Impact Propagation Engine & Cascade Pipeline",
        width=Inches(5.0)
    )

    # 19.6 Scenario Simulation
    add_heading_2(doc, "19.6 What-If Scenario Simulation Studio (Route: `/simulation`)")
    add_paragraph(
        doc,
        "• Purpose: In-memory copy-on-write simulation of operational disruption shocks.\n"
        "• User Problem: Planners cannot test risky contingency plans on production ERP databases without corrupting operational data.\n"
        "• UI Components: 5 Disruption Tabs (Supplier Cut, Route Severance, Demand Surge, WH Shutdown, Combined Compound), "
        "parameter sliders, Non-destructive State Isolation badge, and side-by-side Before vs. After State Comparison tables.\n"
        "• Data Sources: `POST /api/v1/scenario/simulate`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/06_scenario_simulation.png",
        "Figure 19.7 — Screen 6: What-If Scenario Simulation Studio & State Comparison",
        width=Inches(5.0)
    )

    # 19.7 Optimization Engine
    add_heading_2(doc, "19.7 Google OR-Tools Optimization Engine Screen (Route: `/optimize`)")
    add_paragraph(
        doc,
        "• Purpose: Interactive multi-echelon cost optimization comparing un-optimized heuristics against Google OR-Tools.\n"
        "• User Problem: Emergency procurement and rerouting are historically executed via guesswork, resulting in massive SLA penalties.\n"
        "• UI Components: Optimization Setup controls (Disrupted vendor, capacity loss slider, duration slider, risk penalty weight slider), "
        "Solve button, Financial Impact Banner ('Saved 49% - 53% versus baseline heuristic'), and side-by-side Baseline vs. NEXUS metric cards.\n"
        "• Data Sources: `POST /api/v1/optimize`, `GET /api/v1/optimization-runs`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/07_optimization_engine.png",
        "Figure 19.8 — Screen 7: Google OR-Tools Multi-Echelon Optimization Engine",
        width=Inches(5.0)
    )

    # 19.8 Recommendation Center
    add_heading_2(doc, "19.8 Strategic Recommendation Center Screen (Route: `/recommendations`)")
    add_paragraph(
        doc,
        "• Purpose: Translating mathematical optimization solutions into executive-actionable mitigation directives.\n"
        "• User Problem: Senior executives need concise, quantified business decisions rather than thousands of mathematical linear variables.\n"
        "• UI Components: Top Summary KPI Cards (Generated Directives 20, Plan Robustness Index 94%, Simulated ERP Dispatches 0, Est. Operations Cost ₹38.72 Cr), "
        "Directive Action Cards, Root Cause & Risk Rationale callout, Solution Economics breakdown, and 'Simulate ERP/WMS Dispatch' button.\n"
        "• Data Sources: `GET /api/v1/recommendations`."
    )
    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/08_recommendation_center.png",
        "Figure 19.9 — Screen 8: Strategic Recommendation Center & Mitigation Directives",
        width=Inches(5.0)
    )

    doc.add_page_break()
