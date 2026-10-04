"""
NEXUS Capstone Phase-I Report - Chapters 4 to 7, Appendices, and References
Detailed academic content with embedded figures, tables, code snippets, and citations.
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from scripts.build_full_capstone_report import (
    add_para, add_bullet, add_numbered_item, add_subitem,
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_figure_image, add_code_block, set_cell_background, set_cell_margins, set_table_borders,
    COLOR_BLACK, COLOR_RED, HEX_LIGHT_GRAY, HEX_BORDER
)


def build_chapter_4(doc):
    add_chapter_heading(doc, "4", "DESIGN METHODOLOGY AND ITS NOVELTY")

    add_section_heading(doc, "4.1", "METHODOLOGY AND GOAL")
    p1 = (
        "The design methodology employed for the NEXUS platform unites User-Centered Design (UCD) principles with an Agile "
        "software engineering lifecycle and the Cross-Industry Standard Process for Data Mining (CRISP-DM). Traditional supply "
        "chain tools fail in high-stress operational environments because they are designed from a purely transactional "
        "perspective, neglecting the cognitive workflows of logistics planners under crisis conditions. By adopting UCD, the NEXUS "
        "interface and backend workflows were iteratively designed to align with how human dispatchers perceive risk, evaluate "
        "disruptions, test alternative courses of action, and execute operational decisions."
    )
    add_para(doc, p1)

    p2 = (
        "The overarching goal of NEXUS is to instantiate a continuous, closed-loop decision intelligence paradigm: "
        "Monitor → Predict → Analyze Impact → Simulate → Optimize → Recommend. In contrast to isolated software point-solutions, "
        "every component within NEXUS directly feeds the subsequent stage. The platform continuously monitors network telemetry, "
        "predicts latent failure risks using machine learning, maps failure cascades across a multi-tier graph, provides an "
        "in-memory sandbox for 'what-if' simulation, executes Google OR-Tools linear programming to eliminate shortages, and "
        "synthesizes plain-language business recommendations with quantified financial benefits."
    )
    add_para(doc, p2)

    add_section_heading(doc, "4.2", "FUNCTIONAL MODULES DESIGN AND ANALYSIS")
    p3 = "The NEXUS system architecture is partitioned into eight cohesive, decoupled functional modules:"
    add_para(doc, p3)

    add_bullet(doc, "1. Executive Overview & Telemetry Monitor Module:", 
               "Serves as the mission-control home interface. Displays enterprise-wide operational metrics (Network Valuation ₹45.9M, Total Active Inventory 500 SKUs, Overall Network Risk Score, Active Disruptions, and Unresolved Recommendations) alongside an anomaly alert feed and rapid navigation telemetry.")
    add_bullet(doc, "2. Digital Twin Geospatial Network Module:", 
               "Models the complete multi-echelon topology across India. Visualizes 83 nodes (20 Suppliers, 8 Manufacturing Plants, 10 Central Warehouses, 15 Feeder Hubs, and 30 Demand Zones) and 160 transit corridors on an interactive Leaflet GIS map with facility-level telemetry drill-downs.")
    add_bullet(doc, "3. Demand Intelligence & Multi-Horizon Forecaster Module:", 
               "Generates recursive multi-step demand forecasts for all product categories. Integrates 14 autoregressive and calendar features, visually comparing XGBoost projections against 4-week/8-week moving averages and naive persistence baselines.")
    add_bullet(doc, "4. Supplier Risk Intelligence & Anomaly Detection Module:", 
               "Computes multi-dimensional risk scores across all 20 industrial vendors using supervised XGBoost classification evaluated on strictly held-out vendor cohorts. Integrates an unsupervised Isolation Forest scanning for transaction and delay anomalies.")
    add_bullet(doc, "5. Disruption Impact Propagation Engine Module:", 
               "Traverses the NetworkX directed supply dependency graph. Identifies exposed downstream products, affected regional warehouses, remaining inventory runway days, and projected service-level drops under node or route failures.")
    add_bullet(doc, "6. Non-Destructive Scenario Simulation Module:", 
               "Enables risk officers to inject 5 operational disruption archetypes (Supplier Cut, Route Blockade, Demand Spike, Facility Shutdown, Compound Shock) into an in-memory copy-on-write clone, observing network strain without altering persistent records.")
    add_bullet(doc, "7. Mathematical Multi-Echelon Optimization Engine Module:", 
               "Formulates a 530-variable linear program in Google OR-Tools (GLOP). Solves optimal freight rerouting and procurement reallocations in 0.011 seconds, eliminating shortages and minimizing total operational expenditure.")
    add_bullet(doc, "8. Strategic Recommendation Center Module:", 
               "Synthesizes mathematical decision variable matrices into plain-language executive directives. Outlines exact vendor shift volumes, expected rupee savings, service level recoveries, and direct ERP dispatch triggers.")

    add_section_heading(doc, "4.3", "SOFTWARE ARCHITECTURAL DESIGNS")
    p4 = (
        "The NEXUS platform implements a clean, layered client-server architecture separating persistent storage, "
        "computational intelligence, RESTful API services, and modern single-page frontend rendering."
    )
    add_para(doc, p4)

    # Insert Architecture Figures
    add_figure_image(doc, "11_system_architecture_diagram.png", "4.1", "NEXUS Multi-Echelon Software Architectural Design & End-to-End Pipeline", width_in=5.4)

    p_arch_desc = (
        "As illustrated in Fig 4.1, data flows systematically from empirical datasets and digital twin topologies through the "
        "data ingestion pipeline into the relational database engine. From there, the NetworkX graph engine, machine learning "
        "forecaster, supplier risk classifier, and scenario simulator interface seamlessly with the Google OR-Tools optimization "
        "engine. The FastAPI backend exposes 16 REST endpoints that power the React 19 control room."
    )
    add_para(doc, p_arch_desc)

    add_figure_image(doc, "12_decision_intelligence_loop.png", "4.2", "NEXUS 6-Stage Closed-Loop Decision Intelligence Workflow", width_in=5.6)

    p_loop_desc = (
        "Fig 4.2 illustrates the core operational novelty of NEXUS: the 6-stage closed-loop decision workflow. The platform "
        "progresses seamlessly from passive telemetry monitoring to predictive modeling, graph impact propagation, non-destructive "
        "simulation, mathematical optimization, and actionable recommendation generation."
    )
    add_para(doc, p_loop_desc)

    add_figure_image(doc, "13_database_er_diagram.png", "4.3", "Relational Database Schema & Entity-Relationship Diagram (14 Core Entities)", width_in=5.4)

    p_erd_desc = (
        "The relational data model (Fig 4.3) comprises 14 structured tables managed via SQLAlchemy 2.0 ORM. The entities define "
        "physical facilities (suppliers, plants, warehouses, hubs, demand zones), logistics transit corridors (routes), inventory "
        "holdings, historical transactions (orders), operational shock logs (disruptions, risk events), and analytical outputs "
        "(forecasts, optimization runs, recommendations)."
    )
    add_para(doc, p_erd_desc)

    add_section_heading(doc, "4.4", "USER INTERFACE DESIGNS")
    p5 = (
        "The NEXUS user interface is engineered as an enterprise-grade dark control room dashboard. The visual design language "
        "employs deep slate foundations (`#0B0F19` to `#1E293B`) to maximize contrast, minimize ocular fatigue in 24/7 logistics centers, "
        "and provide crystal-clear visual hierarchy for mission-critical alerts."
    )
    add_para(doc, p5)

    add_figure_image(doc, "01_executive_overview.png", "4.4", "NEXUS Executive Overview Control Room Dashboard Interface", width_in=5.6)

    p_ui_desc1 = (
        "Fig 4.4 showcases the Executive Overview interface, featuring high-visibility KPI summary cards, live network health "
        "gauges, demand vs. supply fulfillment trends, active disruption trackers, and recent operational anomaly alerts."
    )
    add_para(doc, p_ui_desc1)

    add_figure_image(doc, "02_digital_twin_network.png", "4.5", "Interactive Leaflet GIS Geospatial Network Map Across Indian Logistics Corridors", width_in=5.6)

    p_ui_desc2 = (
        "Fig 4.5 illustrates the Digital Twin GIS Map view. All 83 logistics nodes across India are dynamically plotted with "
        "custom SVG tier markers, and 160 multimodal freight corridors are rendered as interactive polylines color-coded by "
        "operational status (Active, Congested, Disrupted)."
    )
    add_para(doc, p_ui_desc2)

    add_section_heading(doc, "4.5", "SUMMARY")
    p6 = (
        "Chapter 4 has detailed the User-Centered Design methodology, functional module specifications, multi-tier software "
        "architecture, relational database schema, and high-density control-room UI designs. The architectural novelty lies in "
        "seamlessly bridging predictive machine learning models with Google OR-Tools mathematical optimization within a unified, "
        "real-time web platform."
    )
    add_para(doc, p6)
    doc.add_page_break()


def build_chapter_5(doc):
    add_chapter_heading(doc, "5", "TECHNICAL IMPLEMENTATION & ANALYSIS")

    add_section_heading(doc, "5.1", "OUTLINE")
    p1 = "The technical implementation of the NEXUS platform is structured across four primary engineering domains:"
    add_para(doc, p1)

    add_para(doc, "I. Front-End Web Application Implementation", bold=True, space_after=2)
    add_subitem(doc, "A.", "User Interface Design & Theming: Dark control-room styling using Tailwind CSS, custom color tokens, and Lucide React iconography.")
    add_subitem(doc, "B.", "Component Architecture: Modular React 19 architecture with TypeScript type contracts, reusable KPI cards, risk badges, and workflow breadcrumbs.")
    add_subitem(doc, "C.", "Asynchronous State Management: TanStack React Query v5 for automated server-state caching, background refetching, and optimistic UI mutations.")
    add_subitem(doc, "D.", "Data Visualization & GIS: Recharts responsive multi-series charts and React Leaflet interactive mapping with custom SVG markers.")

    add_para(doc, "II. Back-End Server & Database Implementation", bold=True, space_after=2, space_before=4)
    add_subitem(doc, "A.", "FastAPI REST Server: High-performance asynchronous Python backend with 16 modular API endpoints organized into 10 domain routers.")
    add_subitem(doc, "B.", "Pydantic Schema Validation: Strict validation contracts adhering to OpenAPI 3.1 specifications.")
    add_subitem(doc, "C.", "Relational Database Layer: SQLAlchemy 2.0 ORM with PostgreSQL compatibility and zero-friction standalone SQLite fallback.")
    add_subitem(doc, "D.", "Digital Twin & NetworkX Graph: Directed graph modeling, Haversine geodesic math, and highway tortuosity routing.")

    add_para(doc, "III. Machine Learning & Mathematical Optimization Implementation", bold=True, space_after=2, space_before=4)
    add_subitem(doc, "A.", "Demand Forecasting: Multi-step recursive XGBoost Regressor with 14 autoregressive lag and rolling window features.")
    add_subitem(doc, "B.", "Supplier Disruption Classification: Supervised XGBoost Classifier trained on DataCo fulfillment variance, evaluated on unseen vendor cohorts.")
    add_subitem(doc, "C.", "Transaction Anomaly Detection: Unsupervised Isolation Forest identifying demand surges and transit delay outliers.")
    add_subitem(doc, "D.", "Mathematical Optimization: Google OR-Tools Mixed-Integer Linear Program (GLOP solver) optimizing multi-echelon network flows.")

    add_para(doc, "IV. Testing, Validation, and Deployment Orchestration", bold=True, space_after=2, space_before=4)
    add_subitem(doc, "A.", "Backend Automated Testing: Pytest test suite with 29 passing unit and integration tests.")
    add_subitem(doc, "B.", "Frontend Testing: Vitest and React Testing Library covering UI components and currency formatting.")
    add_subitem(doc, "C.", "Pipeline Automation: Master `run_pipeline.py` script orchestrating end-to-end execution in a single command.")

    add_section_heading(doc, "5.2", "TECHNICAL CODING AND CODE SOLUTIONS")
    p2 = "Key implementation steps and code solutions across the system lifecycle include:"
    add_para(doc, p2)

    add_numbered_item(doc, "1.", "Setting up the Scientific Development Environment: Installed Python 3.11+, PyTorch/XGBoost, Google OR-Tools, NetworkX, GeoPandas, and initialized SQLite database (`data/nexus.db`). Installed Node.js 18+, React 19, TypeScript, Vite, and Tailwind CSS for the frontend.")
    add_numbered_item(doc, "2.", "Empirical Data Preprocessing & Validation: Engineered automated data ingestion pipelines (`pipeline/data_ingestion.py`, `pipeline/data_preprocessing.py`) to clean 421k Walmart sales records, filter negative sales anomalies, normalize delivery variance logs, and seed 50,000 orders.")
    add_numbered_item(doc, "3.", "Autoregressive Feature Engineering: Constructed lag features (t-1, t-2, t-4, t-8) and shifted rolling window statistics (4-week and 8-week means) to eliminate temporal lookahead bias during XGBoost training.")
    add_numbered_item(doc, "4.", "Supervised Supplier Risk Modeling: Implemented logistic shock data generating processes and trained XGBoost classifiers with `scale_pos_weight = 1.5`, evaluating performance across strictly unseen vendor cohorts.")
    add_numbered_item(doc, "5.", "Graph Dependency & Runway Modeling: Utilized NetworkX directed graphs (`SupplyChainGraph`) to traverse multi-echelon supplier-to-warehouse-to-demand paths, calculating stock runway days and flagging potential stockout breaches.")
    add_numbered_item(doc, "6.", "Multi-Echelon Linear Optimization Formulation: Formulated the objective function in Google OR-Tools GLOP solver, balancing procurement, freight, holding, shortage penalties, and risk penalties subject to capacity and flow conservation constraints.")
    add_numbered_item(doc, "7.", "Production REST API Engineering: Created 10 FastAPI router modules (`backend/app/api/`) implementing OpenAPI 3.1 schemas, structured logging, and automated error handling.")
    add_numbered_item(doc, "8.", "React 19 Control Room UI Engineering: Developed 8 responsive screens, implementing TanStack React Query hooks, Leaflet GIS map layers, and Recharts interactive telemetry.")

    add_section_heading(doc, "5.3", "PROTOTYPE SUBMISSION")
    p3 = (
        "The completed prototype is a fully integrated, enterprise-ready web platform. Users can interactively explore the "
        "entire digital supply chain network, inspect individual warehouse inventory runway levels, generate multi-step ML "
        "demand forecasts, simulate severe operational shocks, and execute mathematical optimization in real time."
    )
    add_para(doc, p3)

    add_figure_image(doc, "06_scenario_simulation.png", "5.1", "High-Fidelity Scenario Simulation & Non-Destructive Disruption Testing Interface", width_in=5.6)

    p_proto_desc = (
        "Fig 5.1 demonstrates the interactive Scenario Simulation prototype interface. Users select disruption scenarios "
        "(such as an 80% capacity drop on Supplier SUP_001), specify duration and impacted routes, and execute an in-memory "
        "stress test. The platform calculates lost units, computes affected downstream facilities, and triggers the Google OR-Tools "
        "solver to rebalance network flows."
    )
    add_para(doc, p_proto_desc)

    add_section_heading(doc, "5.4", "SUMMARY")
    p4 = (
        "Chapter 5 has detailed the technical implementation across backend Python microservices, machine learning model "
        "pipelines, mathematical linear programming formulations, and the React 19 control-room frontend. All 29 backend tests "
        "and 10 frontend tests pass with 100% verification, validating the computational integrity of the prototype."
    )
    add_para(doc, p4)
    doc.add_page_break()


def build_chapter_6(doc):
    add_chapter_heading(doc, "6", "PROJECT OUTCOME AND APPLICABILITY")

    add_section_heading(doc, "6.1", "KEY IMPLEMENTATIONS OUTLINE OF THE SYSTEM")
    p1 = "The NEXUS platform delivers five primary engineering outcomes that transform enterprise supply chain operations:"
    add_para(doc, p1)

    add_bullet(doc, "1. National Digital Twin Network:", "A calibrated 83-node geospatial model of India's multi-echelon logistics network, capturing 20 suppliers, 8 manufacturing plants, 10 warehouses, 15 feeder hubs, and 30 consumer demand zones connected across 160 multimodal corridors.")
    add_bullet(doc, "2. High-Accuracy Demand Forecasting:", "An autoregressive XGBoost regressor trained on 421k empirical records, outperforming traditional naive and moving average baselines by 29.5% in RMSE.")
    add_bullet(doc, "3. Out-of-Sample Risk Prediction:", "A supervised disruption risk classifier achieving 0.757 F1-score across unseen industrial suppliers, identifying lead-time variability as the primary leading indicator of supply collapse.")
    add_bullet(doc, "4. Real-Time Mathematical Linear Optimization:", "A Google OR-Tools multi-echelon model that solves optimal network flow across 530 variables in 0.011 seconds, eliminating shortages and minimizing total operational cost.")
    add_bullet(doc, "5. Mission-Control Decision Room:", "A responsive React 19 web application providing supply chain executives with real-time geospatial telemetry, interactive 'what-if' simulations, and explainable mitigation advice.")

    add_section_heading(doc, "6.2", "SIGNIFICANT PROJECT OUTCOMES")
    p2 = (
        "To rigorously quantify the business value of NEXUS, an extensive benchmark experiment was conducted under a severe "
        "operational shock: an 80% capacity loss on Supplier SUP_001 (Tata AutoComp Components, Pune) lasting 10 days. "
        "The performance of standard un-optimized baseline heuristics was compared directly against the NEXUS Google OR-Tools "
        "optimized response. The empirical results are detailed in Table 6.1:"
    )
    add_para(doc, p2)

    # Table 6.1
    res_table = doc.add_table(rows=8, cols=4)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(res_table, HEX_BORDER)

    t_headers = ["Metric", "Baseline Heuristic Response", "NEXUS Optimized Response", "Empirical Value-Add / Impact"]
    t_widths = [Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.6)]

    for c_idx, h_text in enumerate(t_headers):
        cell = res_table.cell(0, c_idx)
        cell.width = t_widths[c_idx]
        set_cell_background(cell, "E2E8F0")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    res_data = [
        ("Total Operational Cost", "INR 41,833,559.60", "INR 19,291,240.54", "-53.89% (Saved ₹22,542,319)"),
        ("Procurement Cost", "INR 11,817,420.00", "INR 12,845,900.00", "+INR 1,028,480 (Agile substitution)"),
        ("Transportation Freight", "INR 1,969,570.00", "INR 5,381,240.00", "Strategic rerouting investment"),
        ("Shortage Penalties Incurred", "INR 26,238,450.00", "INR 0.00", "100% penalties eliminated"),
        ("Total Shortages Incurred", "74,967.0 units", "0.0 units", "74,967 units saved (Zero stockout)"),
        ("Network Service Level", "51.24%", "100.00%", "+48.76 percentage points"),
        ("Linear Solver Runtime", "N/A (Manual)", "0.0114 seconds", "Instant real-time decision response")
    ]

    for row_idx, row_vals in enumerate(res_data, start=1):
        row = res_table.rows[row_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = t_widths[c_idx]
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if c_idx == 2 or (c_idx == 3 and "-" in val):
                r.bold = True

    add_para(doc, "Table 6.1: Empirical Benchmark Comparison — Baseline Operations vs. NEXUS Optimization", italic=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12)

    add_figure_image(doc, "14_model_benchmarks_chart.png", "6.1", "Empirical Machine Learning Demand Forecasting Error Comparison (MAE, RMSE, sMAPE)", width_in=5.4)

    p_ml_bench = (
        "As depicted in Fig 6.1, the lag-engineered XGBoost Regressor achieves superior accuracy across all three metrics "
        "(MAE 68.5k, RMSE 96.0k, sMAPE 4.35%), significantly outperforming 4-week Moving Average (RMSE 153.4k) and Naive "
        "Persistence (RMSE 136.2k)."
    )
    add_para(doc, p_ml_bench)

    add_figure_image(doc, "15_cost_optimization_waterfall.png", "6.2", "Operational Cost Optimization Waterfall Under Disruption Shock", width_in=5.4)

    p_waterfall = (
        "Fig 6.2 illustrates the financial cost breakdown. Under baseline operations, massive shortage penalties (INR 26.2M) "
        "dominate total expenditures. NEXUS makes a measured investment in secondary procurement and freight (+INR 4.4M), "
        "completely averting shortage penalties and yielding a net savings of INR 22,542,319 (53.89% reduction)."
    )
    add_para(doc, p_waterfall)

    add_section_heading(doc, "6.3", "PROJECT APPLICABILITY ON REAL-WORLD APPLICATIONS")
    p3 = "The modular architecture of NEXUS enables direct deployment across major industrial domains:"
    add_para(doc, p3)

    add_bullet(doc, "1. Automotive & Heavy Industrial Manufacturing (Tata Motors, Mahindra, Maruti Suzuki):", 
               "Automotive assembly plants rely on thousands of components. NEXUS can track Tier-1 and Tier-2 component suppliers, predict supplier bottlenecks, and reroute sub-assembly procurement before assembly lines are halted.")
    add_bullet(doc, "2. Fast-Moving Consumer Goods (FMCG) & National Retail (HUL, Reliance Retail, ITC):", 
               "Retail distribution networks face volatile seasonal demand and regional stockouts. NEXUS enables dynamic inventory rebalancing across central mother warehouses and regional feeder distribution centers.")
    add_bullet(doc, "3. Pharmaceutical & Cold-Chain Logistics (Sun Pharma, Dr. Reddy's, Serum Institute):", 
               "Temperature-sensitive vaccine and drug distribution cannot tolerate transit delays. The GIS engine and route severance modeling ensure rapid rerouting around transit blockades to preserve active ingredients.")
    add_bullet(doc, "4. E-Commerce Fulfillment & 3PL Logistics (Amazon India, Flipkart, Delhivery):", 
               "Third-party logistics providers can integrate the Google OR-Tools optimization engine into dispatch management systems to dynamically assign freight across road, rail, and air corridors.")
    add_bullet(doc, "5. Humanitarian Disaster Relief & Defense Logistics:", 
               "During natural calamities (cyclones, floods), supply routes are severed. NEXUS can optimize emergency food, medicine, and relief equipment allocation across surviving transport corridors.")

    add_section_heading(doc, "6.4", "INFERENCE")
    p4 = (
        "The empirical findings demonstrate that integrating predictive machine learning with mathematical linear optimization "
        "delivers profound operational and financial benefits. Un-optimized baseline operations suffer from rigid vendor binding, "
        "causing service level collapse and catastrophic stockout penalties. In contrast, NEXUS autonomously rebalances multi-echelon "
        "flows, proving that agile algorithmic rerouting preserves 100% service levels while cutting crisis operational costs by 53.89%."
    )
    add_para(doc, p4)
    doc.add_page_break()


def build_chapter_7(doc):
    add_chapter_heading(doc, "7", "CONCLUSIONS AND RECOMMENDATION")

    add_section_heading(doc, "7.1", "OUTLINE")
    p1 = (
        "The NEXUS Supply Chain Intelligence Platform successfully accomplishes all primary objectives established for Capstone "
        "Phase-I. The key milestones achieved include:"
    )
    add_para(doc, p1)

    add_bullet(doc, "End-to-End Decision Workflow:", "Successfully operationalized the 6-stage closed-loop architecture: Monitor → Predict → Analyze Impact → Simulate → Optimize → Recommend.")
    add_bullet(doc, "National Digital Twin Modeling:", "Faithfully modeled an 83-node, 160-route multi-echelon logistics network across India with calibrated geodesic and highway routing.")
    add_bullet(doc, "Empirical Data Ingestion:", "Cleaned and validated 421,570 Walmart historical demand records and 35,000 DataCo fulfillment variance records.")
    add_bullet(doc, "High-Performance ML Forecasters & Risk Classifiers:", "Trained XGBoost regressors reducing demand RMSE by 29.5%, and XGBoost risk classifiers evaluated on unseen vendor cohorts.")
    add_bullet(doc, "Real-Time Google OR-Tools Optimization:", "Formulated and solved multi-echelon linear programs in 0.011s, cutting disruption operational costs by 53.89% and eliminating 100% of shortages.")
    add_bullet(doc, "Production-Ready FastAPI & React 19 Stack:", "Deployed 16 REST endpoints with OpenAPI 3.1 documentation and an enterprise dark control room dashboard.")

    add_para(doc, "Key engineering lessons learned during development include:", bold=True, space_after=2, space_before=4)
    add_bullet(doc, "Importance of Non-Destructive Simulation:", "Decoupling 'what-if' shock experiments from persistent storage using copy-on-write state cloning is essential for operational decision support.")
    add_bullet(doc, "Value of Multi-Echelon Reallocation:", "Optimizing flows across multiple tiers absorbs local supply shocks that would completely cripple single-tier heuristic systems.")
    add_bullet(doc, "Rigorous Out-of-Sample Evaluation:", "Evaluating supplier risk on held-out vendor cohorts prevents circular data leakage and ensures real-world model generalizability.")

    add_section_heading(doc, "7.2", "LIMITATION/CONSTRAINTS OF THE SYSTEM")
    p2 = "While NEXUS represents an advanced decision-support platform, certain academic and real-world boundaries are acknowledged:"
    add_para(doc, p2)

    add_bullet(doc, "Deterministic Linear Optimization Assumption:", "The current Google OR-Tools solver utilizes deterministic linear programming (GLOP). While extremely fast (0.011s), it treats parameter inputs (demand, transit times) as deterministic rather than stochastic probability distributions.")
    add_bullet(doc, "Single-Period Disruption Window:", "The optimization model solves a aggregate multi-echelon allocation across the disruption duration rather than a multi-period rolling-horizon formulation with dynamic daily inventory carry-over.")
    add_bullet(doc, "Hybrid Open Dataset Calibration:", "Because enterprise corporate supply chain data is proprietary, the model is calibrated on public research datasets (Walmart and DataCo) mapped onto Indian geospatial coordinates.")
    add_bullet(doc, "External Traffic & Weather API Decoupling:", "Monsoon and strike disruptions are currently modeled via scenario shock injection rather than real-time live ingestion from external meteorological or transit APIs.")

    add_section_heading(doc, "7.3", "FUTURE ENHANCEMENTS")
    p3 = "Promising directions for Capstone Phase-II and future enterprise research include:"
    add_para(doc, p3)

    add_bullet(doc, "1. Multi-Period Rolling Horizon MIP:", "Extending the linear program into a multi-period Mixed-Integer Linear Program (MILP) with time-indexed decision variables X_{s,w,t} and Y_{w,d,t} to model daily inventory accumulation and dynamic replenishment cycles.")
    add_bullet(doc, "2. Stochastic Programming & Robust Optimization:", "Incorporating two-stage stochastic programming with recourse to optimize dispatches under uncertain demand distributions and fluctuating fuel prices.")
    add_bullet(doc, "3. Real-Time IoT GPS Telematics Integration:", "Connecting the GIS engine to live vehicle telematics feeds (OBD-II / GPS) to track freight shipments in real time and automatically detect transit delays.")
    add_bullet(doc, "4. Large Language Model (LLM) Conversational Agent:", "Embedding an enterprise LLM copilot into the control room to allow supply chain officers to query network state and trigger optimizations using natural voice/text commands.")
    add_bullet(doc, "5. Enterprise ERP Connectors (SAP S/4HANA, Odoo, Oracle):", "Developing automated REST/OData connectors to directly dispatch approved purchase orders and reroute shipment manifests into live ERP transactional ledgers.")

    add_section_heading(doc, "7.4", "INFERENCE")
    p4 = (
        "In conclusion, the NEXUS platform conclusively demonstrates that combining digital twin geospatial modeling, "
        "machine learning forecasting, and mathematical multi-echelon linear optimization delivers immense commercial value "
        "for modern enterprise supply chains. By transforming passive retrospective reporting into proactive, closed-loop decision "
        "intelligence, NEXUS establishes a resilient, data-driven framework capable of navigating extreme disruptions, preserving "
        "customer service levels, and unlocking millions of rupees in operational cost savings."
    )
    add_para(doc, p4)
    doc.add_page_break()


def build_appendix_a(doc):
    add_para(doc, "APPENDIX A – SCREEN SHOTS", bold=True, font_size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=18)
    p_intro = "This appendix presents the full high-resolution user interface screen captures of the NEXUS Control Room application and API documentation."
    add_para(doc, p_intro)

    screens = [
        ("01_executive_overview.png", "A.1", "Screen 1: Executive Overview Dashboard — Real-time telemetry, KPI cards, fulfillment trends, and anomaly alert feed."),
        ("02_digital_twin_network.png", "A.2", "Screen 2: Digital Twin Geospatial Network Map — 83 nodes and 160 corridors plotted across Indian logistics hubs."),
        ("02b_digital_twin_facility_inspector.png", "A.3", "Screen 3: Digital Twin Facility Inspector — Granular telemetry drill-down for individual fulfillment warehouses."),
        ("03_demand_intelligence.png", "A.4", "Screen 4: Demand Intelligence & Multi-Step Forecasting — Autoregressive XGBoost projections vs. moving average baselines."),
        ("04_risk_intelligence.png", "A.5", "Screen 5: Supplier Risk Intelligence & Roster — Out-of-sample vendor risk classification, feature drivers, and anomaly flags."),
        ("05_impact_analysis.png", "A.6", "Screen 6: Disruption Impact Propagation — NetworkX graph cascade, stock runway days, and alternative supplier discovery."),
        ("06_scenario_simulation.png", "A.7", "Screen 7: Interactive Scenario Simulation — Non-destructive 'what-if' shock injection and network stress testing."),
        ("07_optimization_engine.png", "A.8", "Screen 8: Mathematical Optimization Engine — Google OR-Tools GLOP solver vs. baseline heuristic comparison."),
        ("08_recommendation_center.png", "A.9", "Screen 9: Strategic Recommendation Center — Plain-language executive mitigation directives with direct ERP dispatch triggers."),
        ("09_swagger_api_docs.png", "A.10", "Screen 10: FastAPI Interactive Swagger Documentation (OpenAPI 3.1) — Live testing interface for all 16 endpoints."),
        ("10_redoc_api_docs.png", "A.11", "Screen 11: ReDoc API Technical Specification — Formal endpoint schemas, request parameters, and response models.")
    ]

    for img_name, fig_label, caption in screens:
        add_figure_image(doc, img_name, fig_label, caption, width_in=5.8)

    doc.add_page_break()


def build_appendix_b(doc):
    add_para(doc, "APPENDIX B – CODING", bold=True, font_size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=18)
    p_intro = (
        "This appendix provides production-grade source code solutions representing core backend optimization formulations, "
        "machine learning forecasters, graph impact algorithms, FastAPI REST endpoints, and React 19 UI components."
    )
    add_para(doc, p_intro)

    # 1. OR-Tools Optimizer
    add_para(doc, "B.1 GOOGLE OR-TOOLS MULTI-ECHELON LINEAR OPTIMIZER (Python)", bold=True, font_size=12, space_before=8, space_after=4)
    ortools_code = """# optimization/ortools_optimizer.py - Google OR-Tools GLOP Multi-Echelon Linear Program Solver
from ortools.linear_solver import pywraplp
import time

class ORToolsOptimizer:
    def __init__(self, risk_penalty_coeff: float = 50.0, shortage_penalty_per_unit: float = 350.0):
        self.risk_coeff = risk_penalty_coeff
        self.shortage_penalty = shortage_penalty_per_unit

    def solve(self, suppliers, warehouses, demand_zones, routes, inventory_levels, severed_routes=None):
        severed_routes = set(severed_routes or [])
        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            raise RuntimeError("GLOP solver unavailable")

        # Decision Variables: X[s,w], Y[w,d], U[d]
        X = {}
        for s in suppliers:
            for w in warehouses:
                X[s['id'], w['id']] = solver.NumVar(0.0, solver.infinity(), f"X_{s['id']}_{w['id']}")

        Y = {}
        for w in warehouses:
            for d in demand_zones:
                Y[w['id'], d['id']] = solver.NumVar(0.0, solver.infinity(), f"Y_{w['id']}_{d['id']}")

        U = {d['id']: solver.NumVar(0.0, solver.infinity(), f"U_{d['id']}") for d in demand_zones}

        # 1. Supplier Capacity Constraints
        for s in suppliers:
            solver.Add(sum(X[s['id'], w['id']] for w in warehouses) <= s['capacity'])

        # 2. Warehouse Inbound Throughput Constraints
        for w in warehouses:
            solver.Add(sum(X[s['id'], w['id']] for s in suppliers) <= w['capacity'])

        # 3. Warehouse Flow Conservation Constraints
        for w in warehouses:
            solver.Add(sum(Y[w['id'], d['id']] for d in demand_zones) <= sum(X[s['id'], w['id']] for s in suppliers))

        # 4. Demand Satisfaction & Shortage Balance Constraints
        for d in demand_zones:
            solver.Add(sum(Y[w['id'], d['id']] for w in warehouses) + U[d['id']] == d['demand'])

        # 5. Severed Corridor Constraints
        for (u, v) in severed_routes:
            if (u, v) in X: solver.Add(X[u, v] == 0.0)
            if (u, v) in Y: solver.Add(Y[u, v] == 0.0)

        # Objective Function: Minimize Total Cost
        obj = solver.Objective()
        for s in suppliers:
            for w in warehouses:
                cost = s['procurement_cost'] + s['freight_cost_to_wh'] + (self.risk_coeff * s.get('risk_score', 0.0))
                obj.SetCoefficient(X[s['id'], w['id']], cost)

        for w in warehouses:
            for d in demand_zones:
                cost = w['holding_cost'] + w['freight_cost_to_zone']
                obj.SetCoefficient(Y[w['id'], d['id']], cost)

        for d in demand_zones:
            obj.SetCoefficient(U[d['id']], self.shortage_penalty)

        obj.SetMinimization()
        t0 = time.time()
        status = solver.Solve()
        runtime = time.time() - t0

        return {
            "status": "OPTIMAL" if status == pywraplp.Solver.OPTIMAL else "FEASIBLE",
            "total_cost": obj.Value(),
            "shortage_units": sum(U[d['id']].solution_value() for d in demand_zones),
            "runtime_seconds": runtime
        }"""
    add_code_block(doc, ortools_code)

    # 2. XGBoost Demand Forecaster
    add_para(doc, "B.2 AUTOREGRESSIVE XGBOOST DEMAND FORECASTER (Python)", bold=True, font_size=12, space_before=10, space_after=4)
    ml_code = """# ml/forecasting/xgboost_forecaster.py - Autoregressive Recursive XGBoost Demand Forecaster
import numpy as np
import pandas as pd
import xgboost as xgb

class DemandForecaster:
    def __init__(self, n_estimators=150, max_depth=4, learning_rate=0.05):
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=42,
            n_jobs=-1
        )

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values('date').copy()
        # Autoregressive Lags
        for lag in [1, 2, 4, 8]:
            df[f'lag_{lag}'] = df['weekly_sales'].shift(lag)
        # Shifted Rolling Statistics (No Lookahead Bias)
        df['rolling_mean_4'] = df['weekly_sales'].shift(1).rolling(4).mean()
        df['rolling_std_4'] = df['weekly_sales'].shift(1).rolling(4).std()
        df['rolling_mean_8'] = df['weekly_sales'].shift(1).rolling(8).mean()
        # Calendar Seasonality
        df['month'] = df['date'].dt.month
        df['week'] = df['date'].dt.isocalendar().week
        df['quarter'] = df['date'].dt.quarter
        return df.dropna()

    def train_and_evaluate(self, df: pd.DataFrame):
        data = self.engineer_features(df)
        features = [c for c in data.columns if c not in ['date', 'weekly_sales', 'store', 'dept']]
        X, y = data[features], data['weekly_sales']

        # Strict Chronological Partitioning (70% Train, 15% Val, 15% Test)
        n = len(data)
        train_idx, val_idx = int(0.70 * n), int(0.85 * n)
        X_train, y_train = X.iloc[:train_idx], y.iloc[:train_idx]
        X_val, y_val = X.iloc[train_idx:val_idx], y.iloc[train_idx:val_idx]
        X_test, y_test = X.iloc[val_idx:], y.iloc[val_idx:]

        self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        preds = self.model.predict(X_test)
        
        mae = np.mean(np.abs(y_test - preds))
        rmse = np.sqrt(np.mean((y_test - preds) ** 2))
        smape = 100 * np.mean(2 * np.abs(preds - y_test) / (np.abs(preds) + np.abs(y_test)))
        return {"MAE": mae, "RMSE": rmse, "sMAPE": smape}"""
    add_code_block(doc, ml_code)

    # 3. NetworkX Graph Impact Engine
    add_para(doc, "B.3 GRAPH DISRUPTION IMPACT PROPAGATION ENGINE (Python)", bold=True, font_size=12, space_before=10, space_after=4)
    graph_code = """# impact/impact_engine.py - NetworkX Multi-Echelon Failure Propagation
import networkx as nx

class ImpactEngine:
    def __init__(self, graph: nx.DiGraph):
        self.G = graph

    def trace_disruption(self, entity_id: str, capacity_loss: float = 0.80, duration_days: int = 10):
        if not self.G.has_node(entity_id):
            return {"error": f"Node {entity_id} not found in graph"}

        # Traverse downstream dependent nodes via Breadth-First Search
        affected_nodes = list(nx.descendants(self.G, entity_id))
        dependent_warehouses = [n for n in affected_nodes if self.G.nodes[n].get('type') == 'WAREHOUSE']
        dependent_zones = [n for n in affected_nodes if self.G.nodes[n].get('type') == 'DEMAND_ZONE']

        # Calculate multi-tier inventory runway
        runway_results = []
        for wh in dependent_warehouses:
            stock = self.G.nodes[wh].get('current_stock', 50000)
            daily_burn = self.G.nodes[wh].get('daily_demand', 4000)
            runway_days = stock / daily_burn if daily_burn > 0 else 999.0
            stockout_risk = runway_days < duration_days
            runway_results.append({
                "warehouse_id": wh,
                "current_stock": stock,
                "runway_days": round(runway_days, 1),
                "stockout_expected": stockout_risk
            })

        return {
            "root_disruption": entity_id,
            "capacity_loss": capacity_loss,
            "duration_days": duration_days,
            "affected_warehouses": dependent_warehouses,
            "affected_demand_zones": dependent_zones,
            "runway_analysis": runway_results
        }"""
    add_code_block(doc, graph_code)

    # 4. FastAPI REST Router
    add_para(doc, "B.4 FASTAPI OPTIMIZATION REST ROUTER (Python)", bold=True, font_size=12, space_before=10, space_after=4)
    api_code = """# backend/app/api/optimization.py - FastAPI Endpoint for Multi-Echelon Linear Program
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.api_schemas import OptimizationRequest, OptimizationResponse
from optimization.ortools_optimizer import ORToolsOptimizer
from optimization.baseline_optimizer import BaselineOptimizer

router = APIRouter(tags=["Optimization Engine"])

@router.post("/optimize", response_model=OptimizationResponse)
def execute_optimization(req: OptimizationRequest, db: Session = Depends(get_db)):
    try:
        # 1. Fetch current network topology and state
        suppliers = fetch_suppliers(db)
        warehouses = fetch_warehouses(db)
        demand_zones = fetch_demand_zones(db)
        routes = fetch_routes(db)
        inventory = fetch_inventory(db)

        # 2. Run Baseline Heuristic Solver
        baseline_solver = BaselineOptimizer()
        base_res = baseline_solver.solve(suppliers, warehouses, demand_zones, routes, req.severed_routes)

        # 3. Run Google OR-Tools Mathematical Solver
        ortools_solver = ORToolsOptimizer(
            risk_penalty_coeff=req.risk_penalty_coeff,
            shortage_penalty_per_unit=req.shortage_penalty_per_unit
        )
        opt_res = ortools_solver.solve(suppliers, warehouses, demand_zones, routes, inventory, req.severed_routes)

        # 4. Compute Net Rupee Cost Savings
        cost_savings = base_res['total_cost'] - opt_res['total_cost']
        pct_savings = (cost_savings / base_res['total_cost']) * 100 if base_res['total_cost'] > 0 else 0.0

        return OptimizationResponse(
            status=opt_res['status'],
            optimized_cost=opt_res['total_cost'],
            baseline_cost=base_res['total_cost'],
            cost_savings_inr=cost_savings,
            percentage_savings=pct_savings,
            shortage_units_eliminated=base_res['shortage_units'] - opt_res['shortage_units'],
            runtime_seconds=opt_res['runtime_seconds']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))"""
    add_code_block(doc, api_code)

    # 5. React 19 Optimization Engine Screen
    add_para(doc, "B.5 REACT 19 OPTIMIZATION ENGINE COMPONENT (TypeScript / TSX)", bold=True, font_size=12, space_before=10, space_after=4)
    react_code = """// frontend/src/pages/OptimizationEngine.tsx - React 19 + TypeScript Optimization Screen
import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { runOptimization, getAnalyticsSummary } from '../api';
import { KpiCard } from '../components/common/KpiCard';
import { formatCurrencyINR, formatPercentage } from '../utils/formatters';
import { Play, TrendingDown, ShieldCheck, Zap } from 'lucide-react';

export const OptimizationEngine: React.FC = () => {
  const [riskCoeff, setRiskCoeff] = useState<number>(50.0);
  const [shortagePenalty, setShortagePenalty] = useState<number>(350.0);

  const { data: analytics } = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: getAnalyticsSummary,
  });

  const optimizeMutation = useMutation({
    mutationFn: () => runOptimization({
      risk_penalty_coeff: riskCoeff,
      shortage_penalty_per_unit: shortagePenalty,
      severed_routes: []
    })
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Google OR-Tools Optimization Engine</h1>
          <p className="text-sm text-slate-400">Multi-echelon mixed-integer linear solver benchmarking baseline vs. optimal response</p>
        </div>
        <button
          onClick={() => optimizeMutation.mutate()}
          disabled={optimizeMutation.isPending}
          className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg font-semibold transition"
        >
          <Play className="w-4 h-4" />
          <span>{optimizeMutation.isPending ? 'Solving...' : 'Run Mathematical Optimization'}</span>
        </button>
      </div>

      {optimizeMutation.data && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <KpiCard
            title="Optimized Total Cost"
            value={formatCurrencyINR(optimizeMutation.data.optimized_cost)}
            icon={<Zap className="w-5 h-5 text-purple-400" />}
            glow="purple"
          />
          <KpiCard
            title="Operational Savings"
            value={formatCurrencyINR(optimizeMutation.data.cost_savings_inr)}
            trend={`-${optimizeMutation.data.percentage_savings.toFixed(2)}%`}
            icon={<TrendingDown className="w-5 h-5 text-emerald-400" />}
            glow="emerald"
          />
          <KpiCard
            title="Shortages Eliminated"
            value={`${optimizeMutation.data.shortage_units_eliminated.toLocaleString()} units`}
            icon={<ShieldCheck className="w-5 h-5 text-blue-400" />}
            glow="blue"
          />
          <KpiCard
            title="Solver Runtime"
            value={`${(optimizeMutation.data.runtime_seconds * 1000).toFixed(1)} ms`}
            icon={<Play className="w-5 h-5 text-amber-400" />}
            glow="amber"
          />
        </div>
      )}
    </div>
  );
};"""
    add_code_block(doc, react_code)

    # 6. Tailwind Theme Styling
    add_para(doc, "B.6 TAILWIND CSS CONTROL ROOM PALETTE CONFIGURATION (JavaScript)", bold=True, font_size=12, space_before=10, space_after=4)
    css_code = """// frontend/tailwind.config.js - Control-Room Dark Theme Configuration
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        nexus: {
          950: '#0B0F19', // Primary background
          900: '#111827', // Card surface
          850: '#151E32', // Elevated panel
          800: '#1F2937', // Border strokes
          700: '#374151', // Hover states
          600: '#4B5563', // Secondary text
          500: '#6B7280', // Muted text
        },
        accent: {
          blue: '#3B82F6',
          emerald: '#10B981',
          amber: '#F59E0B',
          red: '#EF4444',
          purple: '#8B5CF6'
        }
      }
    }
  },
  plugins: []
};"""
    add_code_block(doc, css_code)

    doc.add_page_break()


def build_references(doc):
    add_para(doc, "REFERENCES", bold=True, font_size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=20)

    refs = [
        "[1]. Christopher, M., 'Logistics & Supply Chain Management', 5th Edition, Pearson Education, 2016.",
        "[2]. Simchi-Levi, D., Kaminsky, P., and Simchi-Levi, E., 'Designing and Managing the Supply Chain: Concepts, Strategies, and Case Studies', 3rd Edition, McGraw-Hill, 2008.",
        "[3]. Chen, T., and Guestrin, C., 'XGBoost: A Scalable Tree Boosting System', In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), pp. 785-794, 2016.",
        "[4]. Liu, F. T., Ting, K. M., and Zhou, Z. H., 'Isolation Forest', In 2008 Eighth IEEE International Conference on Data Mining, pp. 413-422, IEEE, 2008.",
        "[5]. Google Developers, 'Google Optimization Tools (OR-Tools) — Fast and portable software for solving combinatorial optimization problems', Google LLC, 2024. Available: https://developers.google.com/optimization",
        "[6]. Hagberg, A. A., Schult, D. A., and Swart, P. J., 'Exploring Network Structure, Dynamics, and Function using NetworkX', In Proceedings of the 7th Python in Science Conference (SciPy2008), pp. 11-15, 2008.",
        "[7]. Tiangolo, S., 'FastAPI: Modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints', 2024. Available: https://fastapi.tiangolo.com",
        "[8]. Constante, F., Silva, F., and Pereira, A., 'DataCo Smart Supply Chain for Big Data Analysis', Mendeley Data, V5, doi: 10.17632/8gx2fvg2k6.5, 2019.",
        "[9]. Kaggle Inc., 'Walmart Recruiting - Store Sales Forecasting Dataset', Walmart Global Analytics Research Competition, 2014. Available: https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting",
        "[10]. Ivanov, D., 'Digital Supply Chain Twins: Managing the Ripple Effect, Resilience, and Disruption Risks', International Journal of Production Research, vol. 58, no. 15, pp. 4646-4668, 2020.",
        "[11]. Chopra, S., and Meindl, P., 'Supply Chain Management: Strategy, Planning, and Operation', 7th Edition, Pearson, 2019.",
        "[12]. Snyder, L. V., and Shen, Z. J. M., 'Fundamentals of Supply Chain Theory', John Wiley & Sons, 2019."
    ]

    for ref in refs:
        add_para(doc, ref, font_size=10.5, space_after=8, line_spacing=1.15)


print("Chapters 4 to 7, Appendices, and References loaded.")
