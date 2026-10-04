"""
NEXUS Report Generator - Part 1:
- Academic Declaration & Disclaimers
- Executive Summary & Abstract
- Table of Contents, List of Figures, List of Tables
- Chapter 1: Introduction
- Chapter 2: Existing Systems & Limitations
- Chapter 3: Proposed System — NEXUS
- Chapter 4: System Architecture
- Chapter 5: Technology Stack
- Chapter 6: Data Sources & Data Pipeline
"""

import os
from docx.shared import Inches, Pt, RGBColor
from scripts.doc_builder_helpers import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_callout,
    add_image_with_caption, add_custom_table, add_equation_block,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DARK_SLATE, COLOR_MUTED, COLOR_BODY
)


def build_preliminaries(doc):
    """Builds academic declarations, abstract, and list catalogs."""
    # -------------------------------------------------------------
    # Academic & Simulation Integrity Declaration
    # -------------------------------------------------------------
    add_heading_1(doc, "Academic & Simulation Integrity Declaration")
    
    add_paragraph(
        doc,
        "I hereby declare that this project report entitled 'NEXUS: AI-Powered Supply Chain Intelligence, "
        "Risk Prediction & Optimization Platform' submitted in partial fulfillment of the requirements for "
        "the award of the degree of Bachelor of Technology in Computer Science & Engineering with Specialization "
        "in Artificial Intelligence & Machine Learning (B.Tech CSE - AI & ML) at Vellore Institute of Technology "
        "(VIT) Bhopal University, is an authentic record of original engineering work carried out by me under academic supervision.",
        bold_prefix="Student Declaration:"
    )

    add_callout(
        doc,
        "ACADEMIC & SIMULATION DATA DISCLAIMER:\n"
        "NEXUS currently operates as an academic decision-intelligence prototype developed for multi-echelon "
        "supply chain modeling, risk forecasting, graph traversal, and mathematical optimization. The platform utilizes "
        "a hybrid empirical foundation: authentic historical time-series demand patterns from the Walmart Store Sales Forecasting "
        "dataset, and empirical fulfillment delay distributions from the DataCo Global Supply Chain dataset, mapped onto a "
        "calibrated synthetic digital twin topology of Indian logistics corridors (83 facilities, 160 multimodal routes).\n\n"
        "Demonstrated scenario outcomes (including modeled cost reductions of 49% to 53% and 100% shortage elimination) are "
        "experimental, mathematical solver-derived results under controlled disruption shocks. They do NOT represent the proprietary "
        "internal operational performance, capacities, or financial records of commercial organizations named in the simulated twin "
        "(e.g., Tata AutoComp, Tata Steel, Foxlink Electronics). NEXUS does not claim live integration with production enterprise ERP, "
        "WMS, or real-time GPS telemetry feeds, as those enterprise backbones are simulated via in-memory state models.",
        alert_type="IMPORTANT",
        title="CRITICAL COMPLIANCE & PROVENANCE NOTICE"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # Executive Summary & Abstract
    # -------------------------------------------------------------
    add_heading_1(doc, "Executive Summary & Abstract")

    add_paragraph(
        doc,
        "Modern enterprise supply chains are vast, highly coupled, multi-echelon networks that span multiple tiers of raw material "
        "suppliers, manufacturing plants, regional central warehouses, cross-dock feeder terminals, and urban consumption markets. "
        "Despite extensive investments in Enterprise Resource Planning (ERP) and Warehouse Management Systems (WMS), enterprise decision-makers "
        "routinely suffer from profound blind spots: operational data remains trapped in transactional silos, forecasting is conducted in "
        "isolation without visibility into supplier operational health, supplier risk assessments are static and backward-looking, and disruption "
        "mitigation relies on fragmented spreadsheet heuristics that react to stockouts only after assembly lines stall and SLA penalties accrue.",
        bold_prefix="Context & Problem Landscape:"
    )

    add_paragraph(
        doc,
        "NEXUS is an enterprise-grade, general-purpose decision-intelligence platform engineered to bridge the gap between predictive AI, "
        "network graph theory, and mathematical optimization. Rather than functioning as a passive reporting dashboard, NEXUS introduces "
        "a closed-loop operational workflow: MONITOR → PREDICT → ANALYZE IMPACT → SIMULATE → OPTIMIZE → RECOMMEND. "
        "The system continuously monitors an authentic Indian logistics digital twin comprising 83 facility nodes and 160 transit corridors, "
        "forecasts multi-horizon SKU demand using an autoregressively engineered XGBoost Regressor (benchmarked against Naive persistence and "
        "Moving Average baselines, achieving a 29.5% RMSE reduction), predicts vendor failure probabilities using a supervised XGBoost classifier "
        "trained with strict group-based out-of-sample vendor isolation to prevent data leakage (F1: 0.757, ROC-AUC: 0.699), and detects real-time "
        "operational outliers via unsupervised Isolation Forests.",
        bold_prefix="The NEXUS Architectural Solution:"
    )

    add_paragraph(
        doc,
        "When an operational disruption occurs—such as an 80% capacity failure at a Tier-1 vendor—NEXUS employs a NetworkX directed graph "
        "traversal engine to trace failure propagation through dependent bills of materials, computing exact warehouse stock runway days "
        "(Runway = Stock / Daily Burn Rate) and identifying imminent stockout breaches before they manifest physically. To resolve the disruption, "
        "the scenario engine creates an in-memory, non-destructive clone of the network state, which is fed into a multi-echelon linear program "
        "solved by Google OR-Tools (GLOP). The optimizer minimizes total operational expenditures across procurement, multimodal freight, warehouse "
        "holding, shortage penalties (INR 350/unit), and risk exposure penalties in just 0.011 seconds. In a demonstrated stress test on Supplier "
        "SUP_001 (Tata AutoComp Components), NEXUS eliminated 100% of unmet shortages (saving 74,967 units), elevated the network service level "
        "from 51.24% to 100.0%, and slashed modeled operational disruption costs by 53.89% (saving INR 22,542,319) compared to standard baseline "
        "operations. Finally, a recommendation engine synthesizes the mathematical solution into plain-language executive directives accompanied "
        "by a mathematically rigorous Plan Feasibility & Robustness Index (0.94 - 0.98).",
        bold_prefix="Quantitative Findings & Impact:"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # Table of Contents
    # -------------------------------------------------------------
    add_heading_1(doc, "Table of Contents")

    toc_items = [
        ("Academic & Simulation Integrity Declaration", "2"),
        ("Executive Summary & Abstract", "3"),
        ("List of Figures", "5"),
        ("List of Tables", "6"),
        ("1. Introduction", "7"),
        ("   1.1 Background & Supply Chain Complexity", "7"),
        ("   1.2 Problem Statement", "8"),
        ("   1.3 Motivation: The Need for Decision Intelligence", "8"),
        ("   1.4 Project Objectives", "9"),
        ("   1.5 System Scope & Boundaries", "9"),
        ("   1.6 Target User Personas & Operational Roles", "10"),
        ("   1.7 Key Technical Contributions", "11"),
        ("2. Existing Systems & Critical Limitations", "12"),
        ("   2.1 Conventional Approaches in Enterprise SCM", "12"),
        ("   2.2 Architectural & Analytical Failure Modes", "13"),
        ("   2.3 Comparative Analysis: Existing Tools vs. NEXUS", "14"),
        ("3. Proposed System — NEXUS Architecture & Decision Loop", "15"),
        ("   3.1 The Closed-Loop Decision Intelligence Cycle", "15"),
        ("   3.2 Six-Stage Functional Decomposition", "16"),
        ("4. Multi-Echelon System Architecture", "18"),
        ("   4.1 Subsystem Layering & Communication Flow", "18"),
        ("   4.2 End-to-End Architectural Topology", "19"),
        ("5. Verified Technology Stack", "21"),
        ("   5.1 Exhaustive Technology Catalog", "21"),
        ("   5.2 Architectural Rationale for Selected Tooling", "23"),
        ("6. Data Sources & Comprehensive Data Pipeline", "25"),
        ("   6.1 Hybrid Data Strategy & Provenance Matrix", "25"),
        ("   6.2 Dataset 1: Walmart Store Sales Time-Series", "26"),
        ("   6.3 Dataset 2: DataCo Global Logistics Supply Chain", "27"),
        ("   6.4 Ingestion, Cleaning & Feature Engineering", "28"),
        ("7. Relational Database Design", "30"),
        ("   7.1 Engine Architecture & Session Management", "30"),
        ("   7.2 Complete 14-Table Relational Schema Catalog", "31"),
        ("   7.3 Entity-Relationship Topology", "34"),
        ("8. Digital Supply Chain Twin (Indian Network)", "36"),
        ("   8.1 Concept of the Calibrated Digital Twin", "36"),
        ("   8.2 Geodesic Coordinates & Indian Industrial Hubs", "37"),
        ("   8.3 Road Network Mathematics & Highway Tortuosity", "38"),
        ("   8.4 Network Topology: Nodes, SKUs, and Corridors", "39"),
        ("   8.5 Inventory Mechanics: Safety Stock & Reorder Points", "41"),
        ("9. Demand Forecasting Engine", "43"),
        ("   9.1 Mathematical Problem Formulation", "43"),
        ("   9.2 Chronological Partitioning & Feature Extraction", "44"),
        ("   9.3 Evaluated Baseline Models & XGBoost Regressor", "45"),
        ("   9.4 Empirical Evaluation & Benchmark Results", "46"),
        ("10. Supervised Supplier Risk Prediction Engine", "48"),
        ("   10.1 Business Rationale & Feature Space", "48"),
        ("   10.2 Resolution of Data Leakage & Group Partitioning", "49"),
        ("   10.3 Logistic Regression vs. XGBoost Classifier", "50"),
        ("   10.4 Feature Importance & Model Explainability", "51"),
        ("11. Operational Anomaly Detection Engine", "53"),
        ("   11.1 Algorithm: Isolation Forest Formulation", "53"),
        ("   11.2 Monitored Signals & Anomaly Taxonomy", "54"),
        ("12. Cascading Impact Propagation Analysis", "56"),
        ("   12.1 NetworkX Directed Graph Modeling", "56"),
        ("   12.2 Multi-Echelon Failure Traversal Algorithm", "57"),
        ("   12.3 Warehouse Stock Runway & Shortage Projection", "58"),
        ("13. Scenario Simulation Studio", "60"),
        ("   13.1 In-Memory Copy-on-Write State Cloning", "60"),
        ("   13.2 Five Verified Disruption Shock Scenarios", "61"),
        ("14. Multi-Echelon Mathematical Optimization Engine", "63"),
        ("   14.1 Linear Programming Model Formulation", "63"),
        ("   14.2 Objective Function & Multi-Cost Tradeoffs", "64"),
        ("   14.3 Constraint Sets (Capacity, Flow, Balance)", "65"),
        ("   14.4 Google OR-Tools GLOP Solver Execution", "66"),
        ("   14.5 Baseline Heuristic Comparison Engine", "67"),
        ("15. Strategic Recommendation Engine", "69"),
        ("   15.1 Mathematical Translation of LP Solution Vectors", "69"),
        ("   15.2 The Plan Feasibility & Robustness Index", "70"),
        ("   15.3 Simulated ERP/WMS Dispatch Interface", "71"),
        ("16. Flagship Demonstration Scenario: Tata AutoComp (SUP_001)", "73"),
        ("   16.1 Step-by-Step Scenario Execution Walkthrough", "73"),
        ("   16.2 Baseline vs. NEXUS Mathematical Comparison", "75"),
        ("   16.3 Anatomy of the 53.89% Cost Reduction", "76"),
        ("17. Backend API Architecture & REST Specification", "78"),
        ("   17.1 FastAPI Framework & Pydantic v2 Contracts", "78"),
        ("   17.2 Complete 16-Endpoint REST Catalog", "79"),
        ("18. Frontend Control Room Architecture", "82"),
        ("   18.1 React 19, TypeScript, and Vite 8.3", "82"),
        ("   18.2 State Management with TanStack React Query", "83"),
        ("   18.3 Code-Splitting, Lazy Loading & Bundle Footprint", "84"),
        ("19. Screen-by-Screen Technical Documentation", "86"),
        ("   19.1 Executive Overview Screen", "86"),
        ("   19.2 Digital Twin Network Map Screen", "88"),
        ("   19.3 Demand Intelligence & Forecasting Screen", "90"),
        ("   19.4 Risk Intelligence Command Screen", "92"),
        ("   19.5 Disruption Impact Propagation Screen", "94"),
        ("   19.6 Scenario Simulation Studio Screen", "96"),
        ("   19.7 Google OR-Tools Optimization Engine Screen", "98"),
        ("   19.8 Strategic Recommendation Center Screen", "100"),
        ("20. End-to-End API → Backend → Frontend Data Flow", "102"),
        ("21. Consolidated Model Performance & Audit Findings", "105"),
        ("22. System Testing & Quality Verification", "108"),
        ("   22.1 Backend Pytest Suite (29/29 Passing)", "108"),
        ("   22.2 Frontend Vitest Suite (10/10 Passing)", "110"),
        ("   22.3 Production Build Verification", "111"),
        ("23. Security, Robustness & Reliability", "112"),
        ("24. System Performance & Efficiency Benchmarks", "114"),
        ("25. Limitations & Academic Boundaries", "116"),
        ("26. Future Scope & Research Roadmap", "118"),
        ("27. Codebase Structure & Architecture Inventory", "120"),
        ("28. Important Code Snippets & Annotated Walkthroughs", "123"),
        ("29. Mathematical Foundations Compendium", "131"),
        ("30. Comprehensive User & Deployment Guide", "136"),
        ("31. 5-Minute Project Demonstration Script", "140"),
        ("32. Viva Voce Preparation Handbook (55 Questions & Answers)", "143"),
        ("33. Technical Glossary", "160"),
        ("34. Conclusion & Final Remarks", "164"),
        ("35. Appendices (A through H)", "166")
    ]

    toc_data = [[title, page] for title, page in toc_items]
    add_custom_table(
        doc,
        headers=["Section / Chapter Title", "Target Page"],
        data=toc_data,
        col_widths=[Inches(5.3), Inches(1.2)],
        alignment=['L', 'R']
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # List of Figures & List of Tables
    # -------------------------------------------------------------
    add_heading_1(doc, "List of Figures")

    fig_items = [
        ("Figure 3.1", "The NEXUS Closed-Loop Decision Intelligence Cycle", "Chapter 3"),
        ("Figure 4.1", "NEXUS Multi-Echelon System Architecture Topology", "Chapter 4"),
        ("Figure 7.1", "Relational Database Schema & Entity Relationships (14 Models)", "Chapter 7"),
        ("Figure 9.1", "Demand Forecasting Model Benchmark Error Comparison (RMSE & MAE)", "Chapter 9"),
        ("Figure 10.1", "Supplier Risk Supervised Classification Out-of-Sample Metrics", "Chapter 10"),
        ("Figure 14.1", "Multi-Echelon Cost Breakdown: Baseline Heuristic vs. NEXUS OR-Tools", "Chapter 14"),
        ("Figure 14.2", "Operational Resilience: Service Level Preservation & Shortage Avoidance", "Chapter 14"),
        ("Figure 17.1", "FastAPI Interactive OpenAPI 3.1 Swagger Documentation UI", "Chapter 17"),
        ("Figure 17.2", "Alternative Technical ReDoc Specification Interface", "Chapter 17"),
        ("Figure 19.1", "Screen 1 — Executive Supply Chain Overview Dashboard", "Chapter 19"),
        ("Figure 19.2", "Screen 2 — Digital Supply Chain Twin Geospatial Network Map", "Chapter 19"),
        ("Figure 19.3", "Screen 2b — Interactive Facility Inspector Drawer & Node Telemetry", "Chapter 19"),
        ("Figure 19.4", "Screen 3 — Demand Intelligence & Multi-Horizon Forecasting", "Chapter 19"),
        ("Figure 19.5", "Screen 4 — Supply Chain Risk Command Center & Live ML Inference", "Chapter 19"),
        ("Figure 19.6", "Screen 5 — Disruption Impact Propagation Engine & Cascade Pipeline", "Chapter 19"),
        ("Figure 19.7", "Screen 6 — What-If Scenario Simulation Studio & State Comparison", "Chapter 19"),
        ("Figure 19.8", "Screen 7 — Google OR-Tools Multi-Echelon Optimization Engine", "Chapter 19"),
        ("Figure 19.9", "Screen 8 — Strategic Recommendation Center & Mitigation Directives", "Chapter 19")
    ]

    add_custom_table(
        doc,
        headers=["Figure No.", "Title / Description", "Location"],
        data=fig_items,
        col_widths=[Inches(1.2), Inches(4.3), Inches(1.0)],
        alignment=['L', 'L', 'C']
    )

    add_heading_1(doc, "List of Tables")

    tbl_items = [
        ("Table 2.1", "Comparative Architectural Analysis: Traditional Tools vs. NEXUS", "Chapter 2"),
        ("Table 5.1", "Verified Production Technology Stack & Library Versions", "Chapter 5"),
        ("Table 6.1", "Data Provenance Classification & Source Foundation Matrix", "Chapter 6"),
        ("Table 6.2", "Walmart Store Sales Dataset Specification & Variable Mapping", "Chapter 6"),
        ("Table 6.3", "DataCo Global Supply Chain Dataset Fields & Risk Mapping", "Chapter 6"),
        ("Table 7.1", "Complete Relational Database Model Catalog & Row Counts", "Chapter 7"),
        ("Table 8.1", "Canonical Indian Logistics Hubs Geocoded Coordinates", "Chapter 8"),
        ("Table 9.1", "Autoregressive Lag & Rolling Window Feature Set (14 Variables)", "Chapter 9"),
        ("Table 9.2", "Demand Forecasting Model Benchmark Comparison on Test Set", "Chapter 9"),
        ("Table 10.1", "Supervised Supplier Risk Features & Out-of-Sample Performance", "Chapter 10"),
        ("Table 10.2", "Empirical Feature Importance Attribution of the XGBoost Classifier", "Chapter 10"),
        ("Table 13.1", "Supported Operational Disruption Scenarios & Shock Parameters", "Chapter 13"),
        ("Table 14.1", "Mathematical Linear Program Sets, Parameters, and Variables", "Chapter 14"),
        ("Table 16.1", "Disruption Scenario Audit: Baseline vs. NEXUS OR-Tools Performance", "Chapter 16"),
        ("Table 17.1", "FastAPI RESTful Endpoints Master Reference (16 Endpoints)", "Chapter 17"),
        ("Table 21.1", "Consolidated Machine Learning & Optimization Evaluation Master", "Chapter 21"),
        ("Table 22.1", "Backend Automated Test Suite Verification Results (29 Tests)", "Chapter 22"),
        ("Table 22.2", "Frontend Vitest Automated Test Results (10 Tests)", "Chapter 22"),
        ("Table 24.1", "System Performance, Latency, and Bundle Footprint Benchmarks", "Chapter 24")
    ]

    add_custom_table(
        doc,
        headers=["Table No.", "Table Caption / Description", "Location"],
        data=tbl_items,
        col_widths=[Inches(1.2), Inches(4.3), Inches(1.0)],
        alignment=['L', 'L', 'C']
    )

    doc.add_page_break()


def build_chapter_1(doc):
    """Builds Chapter 1: Introduction."""
    add_heading_1(doc, "1. Introduction")

    add_heading_2(doc, "1.1 Background & Supply Chain Complexity")
    add_paragraph(
        doc,
        "In the contemporary globalized economy, industrial supply chains have evolved from simple linear pipelines into intricate, "
        "hyper-connected multi-echelon networks. Modern manufacturing corporations—ranging from automotive giants and consumer electronics "
        "conglomerates to fast-moving consumer goods (FMCG) and pharmaceutical enterprises—rely on hundreds of specialized suppliers across "
        "multiple tiers of sub-assembly. Finished products are funneled through regional manufacturing plants, consolidated in central fulfillment "
        "depots, partitioned across transit cross-dock hubs, and ultimately distributed to dispersed consumer demand zones."
    )
    add_paragraph(
        doc,
        "While this globalized specialization has maximized production efficiency and reduced baseline unit costs, it has simultaneously "
        "introduced unprecedented systemic fragility. The lean 'Just-In-Time' (JIT) manufacturing paradigms pioneered over recent decades have "
        "deliberately eliminated inventory buffers across every tier of the network. As a consequence, localized disruptions—such as unexpected "
        "factory equipment breakdowns, regional labor disputes, severe monsoon floods, or highway bottlenecks—no longer remain isolated. Instead, "
        "they propagate rapidly downstream, amplifying demand distortion (the classic 'Bullwhip Effect') and triggering catastrophic stockouts at "
        "distant distribution centers."
    )

    add_heading_2(doc, "1.2 Problem Statement")
    add_paragraph(
        doc,
        "Modern enterprise supply chains face three interconnected, compounding points of failure:",
        bold_prefix="The Operational Crisis:"
    )
    add_bullet(
        doc,
        "Enterprise data is fractured across disparate ERP, WMS, and TMS systems. Operations planners lack a unified, "
        "geospatially coherent digital twin of the entire multi-echelon topology, rendering them blind to cross-facility dependencies.",
        bold_prefix="1. Information Silos & Fragmented Visibility:"
    )
    add_bullet(
        doc,
        "Forecasting is historically conducted using basic spreadsheet heuristics or isolated statistical software that ignores "
        "upstream supply constraints. Meanwhile, vendor risk management relies on backward-looking quarterly scorecards that fail to detect "
        "imminent operational failures before deliveries breach SLAs.",
        bold_prefix="2. Decoupled Predictive Intelligence:"
    )
    add_bullet(
        doc,
        "When an unexpected shock strikes (e.g., an 80% loss in capacity at a key supplier), supply chain managers are forced into manual, "
        "ad-hoc firefighting. Lacking automated mathematical optimization tools, they execute rigid single-supplier rules that cause massive stockouts, "
        "service-level collapses, and millions of INR in contractual SLA penalties.",
        bold_prefix="3. Reactive Disruption Firefighting:"
    )

    add_heading_2(doc, "1.3 Motivation: The Need for Decision Intelligence")
    add_paragraph(
        doc,
        "Passive business intelligence dashboards that merely report historical failures ('what went wrong yesterday') are fundamentally inadequate "
        "for modern high-velocity logistics. True supply chain resilience demands an active **Decision Intelligence** platform that answers three "
        "forward-looking operational questions:"
    )
    add_bullet(doc, "What is likely to fail in the network, where, and with what probability?", bold_prefix="1. Predictive Horizon:")
    add_bullet(doc, "If this failure occurs, what exact downstream products, warehouses, and consumer demand zones will suffer stockouts?", bold_prefix="2. Cascading Impact:")
    add_bullet(doc, "What mathematically optimal, cost-minimized reallocation actions should we execute right now to prevent those stockouts?", bold_prefix="3. Prescriptive Recovery:")

    add_heading_2(doc, "1.4 Project Objectives")
    add_paragraph(doc, "The NEXUS project was conceived to achieve nine measurable, verified engineering objectives:")
    add_bullet(doc, "Build an authentic, geocoded Indian digital supply chain twin network modeling 83 facility nodes and 160 transit corridors.", bold_prefix="Obj 1 (Digital Twin):")
    add_bullet(doc, "Integrate real empirical research datasets (Walmart Store Sales, 421k rows; DataCo Logistics, 35k rows) with zero mock data in live execution.", bold_prefix="Obj 2 (Data Foundation):")
    add_bullet(doc, "Train and evaluate an autoregressive XGBoost demand forecasting model that outperforms Naive and Moving Average baselines by at least 25% RMSE reduction.", bold_prefix="Obj 3 (Demand ML):")
    add_bullet(doc, "Develop a supervised supplier disruption classifier using strict out-of-sample vendor grouping to prevent data leakage.", bold_prefix="Obj 4 (Risk ML):")
    add_bullet(doc, "Implement multi-variate unsupervised anomaly detection (Isolation Forest) to flag operational delay and demand volume outliers.", bold_prefix="Obj 5 (Anomaly Detection):")
    add_bullet(doc, "Build a NetworkX graph traversal engine that traces multi-echelon cascading failure paths and computes warehouse stock runways.", bold_prefix="Obj 6 (Impact Engine):")
    add_bullet(doc, "Implement an in-memory, non-destructive scenario simulation studio supporting five distinct operational disruption shocks.", bold_prefix="Obj 7 (Simulation Studio):")
    add_bullet(doc, "Formulate and solve a multi-echelon linear optimization problem using Google OR-Tools (GLOP), proving measurable cost reduction and 100% shortage elimination over baseline heuristics.", bold_prefix="Obj 8 (OR-Tools Optimization):")
    add_bullet(doc, "Deliver a production-ready, dark-palette React 19 control-room frontend with 8 functional screens, interactive Leaflet GIS mapping, Recharts visualizations, and 16 REST endpoints.", bold_prefix="Obj 9 (Full-Stack UI/API):")

    add_heading_2(doc, "1.5 System Scope & Boundaries")
    add_paragraph(
        doc,
        "To ensure academic rigor and feasibility, NEXUS defines explicit system boundaries:\n"
        "• IN SCOPE: Multi-echelon logistics modeling across Tier-1 and Tier-2 suppliers, assembly plants, central warehouses, distribution hubs, and demand zones; "
        "geodesic road distance calculation with highway tortuosity; recursive time-series forecasting; supervised disruption classification; "
        "in-memory scenario state cloning; linear programming cost optimization; explainable recommendation synthesis; FastAPI backend; and React 19 UI.\n"
        "• OUT OF SCOPE: Live production connectors to proprietary enterprise ERP backbones (SAP S/4HANA, Oracle SCM); live IoT GPS telematics streaming; "
        "Tier-4 raw mineral extraction mining modeling; and automated financial fund transfers or purchase order dispatch to external vendors."
    )

    add_heading_2(doc, "1.6 Target User Personas & Operational Roles")
    add_paragraph(doc, "NEXUS is designed for enterprise supply chain professionals across four functional domains:")
    add_bullet(doc, "Uses the Executive Overview and Strategic Recommendation Center to evaluate network risk posture and approve mitigation budgets.", bold_prefix="• Chief Supply Chain Officer (CSCO) & VP of Logistics:")
    add_bullet(doc, "Uses the Risk Command Center and live ML inference sliders to identify vulnerable vendors and adjust sourcing splits before SLA breach.", bold_prefix="• Strategic Procurement Managers:")
    add_bullet(doc, "Uses the Scenario Simulation Studio and Google OR-Tools Optimizer to compute emergency truckload reallocations and detour corridors.", bold_prefix="• Operations & Fulfillment Planners:")
    add_bullet(doc, "Uses Demand Intelligence and Impact Propagation to monitor stock runway days and prevent safety stock breaches.", bold_prefix="• Inventory & Warehouse Controllers:")

    add_heading_2(doc, "1.7 Key Technical Contributions")
    add_paragraph(
        doc,
        "The NEXUS platform delivers five distinct technical contributions to the domain of supply chain engineering:\n"
        "1. Unified Closed-Loop Workflow: Integrates forecasting, risk modeling, graph impact traversal, simulation, and mathematical optimization into a continuous decision cycle.\n"
        "2. Audited Machine Learning Credibility: Eradicates circular synthetic labeling and prevents vendor data leakage via GroupShuffleSplit out-of-sample validation.\n"
        "3. Real-Time Linear Programming: Solves 530 continuous variables across 70 multi-echelon constraints in under 15 milliseconds using Google OR-Tools GLOP.\n"
        "4. Mathematical Plan Robustness Index: Replaces static 'AI confidence' literals with a formal LP solver-derived optimality and shortage mitigation metric.\n"
        "5. Modern Decoupled Web Architecture: Features an asynchronous FastAPI backend paired with a code-split React 19 control room (~365 kB initial load)."
    )

    doc.add_page_break()


def build_chapter_2(doc):
    """Builds Chapter 2: Existing Systems & Limitations."""
    add_heading_1(doc, "2. Existing Systems & Limitations")

    add_heading_2(doc, "2.1 Conventional Approaches in Enterprise SCM")
    add_paragraph(
        doc,
        "Enterprise supply chain management has historically relied on a fragmented patchwork of legacy software and manual procedures:"
    )
    add_bullet(
        doc,
        "Microsoft Excel and Google Sheets remain the default planning tool for over 60% of mid-sized enterprise supply chain teams. "
        "Planners maintain massive workbooks with complex VLOOKUP formulas to estimate monthly procurement needs. These sheets lack dynamic graph topology, "
        "cannot solve multi-echelon optimization problems, and break immediately when sudden disruptions occur.",
        bold_prefix="1. Spreadsheet Heuristics & Static Workbooks:"
    )
    add_bullet(
        doc,
        "Platforms like Microsoft Power BI, Tableau, and Qlik Sense provide attractive operational dashboards. However, they are inherently "
        "retrospective: they display past on-time delivery percentages and current inventory levels without predictive forward projection or automated "
        "prescriptive recovery recommendations.",
        bold_prefix="2. Descriptive Business Intelligence Dashboards:"
    )
    add_bullet(
        doc,
        "Legacy enterprise systems (e.g., SAP ECC, Oracle E-Business Suite) manage transactional records efficiently but process modules in isolation. "
        "Material Requirements Planning (MRP) runs as a batch process overnight, calculating gross inventory requirements based on static lead times "
        "without factoring in dynamic supplier disruption probabilities or road transit risks.",
        bold_prefix="3. Monolithic Transactional ERP Systems:"
    )
    add_bullet(
        doc,
        "Procurement teams evaluate suppliers through subjective annual questionnaires and retrospective SLA breach reports. These mechanisms "
        "provide zero advance warning when a vendor experiences hidden operational strain (e.g., rising lead-time volatility or capacity saturation).",
        bold_prefix="4. Manual Vendor Risk Assessments:"
    )

    add_heading_2(doc, "2.2 Critical Limitations of Conventional Approaches")
    add_paragraph(
        doc,
        "When evaluated against modern supply chain disruptions, conventional paradigms suffer from four fundamental failure modes:\n"
        "• Decoupled Sourcing & Optimization: Sourcing decisions are made by procurement without evaluating the downstream freight cost impact on warehouses, "
        "leading to localized optimization that increases global network costs.\n"
        "• Zero Cascading Failure Visibility: Traditional systems cannot traverse multi-tier graphs. When a component supplier fails, planners cannot "
        "determine which end-consumer demand zones will experience stockouts until customer orders fail to ship.\n"
        "• Rigid Heuristic Sourcing: In a crisis, traditional rule-based heuristics attempt to reorder from secondary vendors using fixed priority lists, "
        "often overwhelming secondary vendor capacity and triggering secondary stockouts.\n"
        "• Latency in Decision Execution: Resolving a major supply shock typically requires days of cross-departmental meetings, email exchanges, "
        "and manual spreadsheet scenario modeling, by which time critical factory assembly lines have already shut down."
    )

    add_heading_2(doc, "2.3 Comparative Analysis: Existing Tools vs. NEXUS")
    
    comp_headers = ["Functional Capability", "Spreadsheets (Excel)", "Descriptive BI (PowerBI)", "Enterprise ERP (MRP II)", "NEXUS Platform"]
    comp_data = [
        ["Network Topology", "None (Tabular rows)", "Geocoded points only", "Hierarchical facility tree", "NetworkX DiGraph (83 nodes)"],
        ["Demand Forecasting", "Linear trend / Holt-Winters", "Static time-series charts", "Historical moving average", "Lag-Engineered XGBoost Regressor"],
        ["Supplier Risk Analysis", "Manual quarterly scorecard", "Historical SLA breach charts", "Rule-based flag upon failure", "Supervised XGBoost Classifier"],
        ["Anomaly Detection", "Manual conditional formatting", "Static threshold alerts", "None / Transaction audit", "Unsupervised Isolation Forest"],
        ["Cascading Impact", "Zero dependency tracing", "Zero graph traversal", "BOM explosion (static)", "Multi-echelon graph propagation"],
        ["What-If Simulation", "Fragile manual formulas", "Limited slicer filtering", "Requires staging clone DB", "In-memory non-destructive state clone"],
        ["Optimization Engine", "Excel Solver (Single node)", "None (Reporting only)", "Linear programming add-on", "Google OR-Tools GLOP (<15 ms)"],
        ["Recommendation Logic", "Human judgment only", "None", "Purchase requisition prompts", "Explainable directives with INR ROI"],
        ["Robustness Index", "None", "None", "None", "Mathematical LP Feasibility Metric"]
    ]

    add_custom_table(
        doc,
        headers=comp_headers,
        data=comp_data,
        col_widths=[Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.3)],
        alignment=['L', 'C', 'C', 'C', 'C'],
        title="Table 2.1 — Comparative Architectural Analysis: Traditional Tools vs. NEXUS"
    )

    doc.add_page_break()


def build_chapter_3(doc):
    """Builds Chapter 3: Proposed System — NEXUS."""
    add_heading_1(doc, "3. Proposed System — NEXUS Architecture & Decision Loop")

    add_heading_2(doc, "3.1 The Closed-Loop Decision Intelligence Cycle")
    add_paragraph(
        doc,
        "To overcome the fatal limitations of disconnected legacy tools, NEXUS establishes a continuous, automated "
        "closed-loop decision cycle. The platform transitions enterprise supply chain operations from reactive crisis firefighting "
        "to proactive predictive mitigation:"
    )

    add_equation_block(
        doc,
        "MONITOR  ──▶  PREDICT  ──▶  ANALYZE IMPACT  ──▶  SIMULATE  ──▶  OPTIMIZE  ──▶  RECOMMEND",
        eq_num="Workflow 3.1",
        explanation="The continuous six-stage closed-loop operational decision cycle implemented across the NEXUS backend and frontend control room."
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/12_decision_intelligence_loop.png",
        "Figure 3.1 — The NEXUS Closed-Loop Decision Intelligence Cycle (Continuous Operational Feedback)",
        width=Inches(5.2)
    )

    add_heading_2(doc, "3.2 Six-Stage Functional Decomposition")
    add_paragraph(doc, "Every phase of the NEXUS decision cycle executes a specialized, mathematically rigorous computational stage:")

    add_paragraph(
        doc,
        "The digital twin maintains a continuous real-time model of the multi-echelon network (83 nodes across 20 suppliers, 8 manufacturing plants, "
        "10 central warehouses, 15 feeder hubs, and 30 demand zones, connected by 160 transit corridors). Unsupervised Isolation Forest models scan order "
        "volumes and transit logs to detect real-time anomalies (e.g., sudden order surges or transit delays exceeding 3σ).",
        bold_prefix="Stage 1: MONITOR (Digital Twin Telemetry & Anomaly Detection):"
    )

    add_paragraph(
        doc,
        "Dual machine learning engines anticipate operational distress before SLA breach. The Demand Forecaster uses a lag-engineered XGBoost Regressor "
        "to project multi-horizon demand trajectories across consumer zones. Simultaneously, the Supplier Risk Engine applies a supervised XGBoost "
        "classifier to evaluate vendor failure probability based on lead-time volatility, delay frequency, capacity strain, and QA acceptance rates.",
        bold_prefix="Stage 2: PREDICT (Demand Forecasting & Supplier Risk Classification):"
    )

    add_paragraph(
        doc,
        "When an entity exhibits critical risk or suffers an operational shock, the NetworkX directed graph engine executes a downstream failure traversal. "
        "It maps the failure from the disrupted node through dependent bills of materials, calculates exact warehouse stock runway days "
        "(Runway = Stock / Daily Burn Rate), and projects potential shortage volumes and service-level degradation across consuming markets.",
        bold_prefix="Stage 3: ANALYZE IMPACT (Graph Cascading Traversal & Runway Math):"
    )

    add_paragraph(
        doc,
        "Before executing recovery actions, decision-makers test hypotheses in the Scenario Simulation Studio. The engine creates an in-memory, "
        "non-destructive clone of the network state (copy-on-write), applying simulated shock transformations (supplier capacity loss, corridor severance, "
        "warehouse shutdown, or demand surges) without mutating the persistent operational database.",
        bold_prefix="Stage 4: SIMULATE (In-Memory Disruption Shock Ingestion):"
    )

    add_paragraph(
        doc,
        "The simulated network state is ingested by Google OR-Tools (GLOP). The optimizer formulates and solves a multi-echelon linear program "
        "comprising 530 continuous decision variables and 70 linear constraints. The model simultaneously minimizes procurement expenditures, multimodal "
        "freight costs, warehouse holding costs, supplier risk exposure penalties, and shortage penalties (INR 350/unit) in ~0.011 seconds.",
        bold_prefix="Stage 5: OPTIMIZE (Google OR-Tools Multi-Echelon Linear Program):"
    )

    add_paragraph(
        doc,
        "The recommendation engine translates the raw mathematical solution vectors into plain-language executive directives (e.g., 'Shift 16.8% of demand "
        "to SUP_005; dispatch 1,800 buffer units from WH_04'). Each directive is accompanied by quantified financial ROI and a mathematically derived "
        "Plan Feasibility & Robustness Index (0.94 - 0.98). Planners can dispatch the strategy directly to a simulated ERP/WMS ingestion queue.",
        bold_prefix="Stage 6: RECOMMEND (Actionable Executive Directives & Plan Robustness):"
    )

    doc.add_page_break()


def build_chapter_4(doc):
    """Builds Chapter 4: System Architecture."""
    add_heading_1(doc, "4. Multi-Echelon System Architecture")

    add_heading_2(doc, "4.1 Subsystem Layering & Communication Flow")
    add_paragraph(
        doc,
        "The NEXUS system architecture is engineered as a highly decoupled, modular multi-tier enterprise platform. "
        "Each subsystem operates with clean separation of concerns, enforcing strict Pydantic v2 data contracts between layers:"
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/11_system_architecture_diagram.png",
        "Figure 4.1 — NEXUS Multi-Echelon System Architecture Topology (6 Integrated Technology Layers)",
        width=Inches(5.2)
    )

    add_heading_2(doc, "4.2 Architectural Layer Breakdown")
    add_paragraph(
        doc,
        "The complete platform comprises six tightly integrated architectural layers:\n"
        "• Layer 1 (Data Foundation): Combines empirical research time-series (Walmart Store Sales, 421k records), logistics variance data (DataCo Global Logistics, 35k records), "
        "canonical Indian geodesic hub coordinates, and calibrated synthetic disruption events.\n"
        "• Layer 2 (Data Pipeline & Ingestion): Orchestrates automated database seeding, schema normalization, missing value imputation, chronological time-series splitting, "
        "and autoregressive lag/rolling window feature extraction.\n"
        "• Layer 3 (Digital Twin & Network Graph): Represents the physical supply chain as an in-memory NetworkX directed graph (83 nodes, 160 corridors), computes betweenness and "
        "degree centrality, tracks 500 SKU warehouse inventory stocks, and models highway road distances with a 1.22x tortuosity factor.\n"
        "• Layer 4 (Predictive & Decision Intelligence): Hosts the core analytical modules—XGBoost Demand Regressor, Supervised Supplier Risk Classifier, Isolation Forest Anomaly Detector, "
        "NetworkX Impact Traversal Engine, Scenario Simulation Studio, Google OR-Tools Linear Solver (GLOP), and Recommendation Synthesizer.\n"
        "• Layer 5 (RESTful API Backend): Built with FastAPI, Uvicorn, and Pydantic v2. Exposes 16 REST endpoints with OpenAPI 3.1 specifications, SQLAlchemy 2.0 ORM database sessions, "
        "and structured JSON logging.\n"
        "• Layer 6 (Enterprise Control Room UI): Built with React 19, TypeScript, Vite 8.3, and Tailwind CSS. Features 8 lazy-loaded control-room screens, interactive Leaflet GIS maps, "
        "Recharts analytics visualizations, and TanStack React Query background cache."
    )

    doc.add_page_break()


def build_chapter_5(doc):
    """Builds Chapter 5: Technology Stack."""
    add_heading_1(doc, "5. Verified Technology Stack")

    add_heading_2(doc, "5.1 Exhaustive Technology Catalog")
    add_paragraph(
        doc,
        "In strict accordance with the project verification rules, every technology, framework, and library listed below has been "
        "directly verified from the repository configuration files (requirements.txt, package.json) and live runtime environments:"
    )

    stack_headers = ["Layer / Subsystem", "Technology / Library", "Verified Version", "Architectural Role in NEXUS"]
    stack_data = [
        ["Runtime Environment", "Python", "3.13.5 (3.11+ compatible)", "Core backend computational runtime and ML execution environment"],
        ["Runtime Environment", "Node.js & npm", "v24.19.0 / npm 11.17.0", "Frontend JavaScript runtime and package manager"],
        ["Backend Web Framework", "FastAPI", "0.115.0+", "High-performance asynchronous REST API framework with automatic OpenAPI 3.1 docs"],
        ["API Data Contracts", "Pydantic", "2.10.0+ (v2)", "Strict runtime type checking, schema validation, and serialization contracts"],
        ["ASGI Web Server", "Uvicorn", "0.34.0+", "Production-grade ASGI server running on port 8000 with auto-reload capabilities"],
        ["Database ORM", "SQLAlchemy", "2.0.0+", "Enterprise Object-Relational Mapping with connection pooling and typed session models"],
        ["Relational Database", "SQLite / PostgreSQL", "SQLite 3 (data/nexus.db)", "Zero-friction standalone database (12.8 MB) with full PostgreSQL DDL compatibility"],
        ["Data Processing", "Pandas", "2.2.0+", "High-performance tabular data manipulation, time-series aggregation, and feature extraction"],
        ["Numerical Computing", "NumPy", "2.0.0+", "Vectorized matrix computations, linear algebra, and mathematical statistics"],
        ["Machine Learning", "Scikit-Learn", "1.6.0+", "Logistic Regression, Isolation Forest, GroupShuffleSplit, StandardScaler, and metrics"],
        ["Gradient Boosting", "XGBoost", "2.1.0+", "Gradient boosted regression trees for demand forecasting and supervised risk classification"],
        ["Model Persistence", "Joblib", "1.4.0+", "High-throughput serialization and deserialization of trained ML model pipelines"],
        ["Network Graph Modeling", "NetworkX", "3.4.0+", "Directed graph modeling, multi-echelon traversal, and betweenness centrality analysis"],
        ["Geospatial Geometry", "Shapely", "2.0.0+", "Geometric point and polygon modeling for Indian logistics hubs"],
        ["Spatial Data Analysis", "GeoPandas", "1.0.0+", "Spatial GeoJSON FeatureCollection generation and geographic coordinate handling"],
        ["Mathematical Solver", "Google OR-Tools", "9.10.0+", "Industrial-grade linear programming solver (GLOP) for multi-echelon network optimization"],
        ["Backend Testing", "Pytest", "9.1.1", "Automated test suite executing 29 verified unit, integration, and API tests"],
        ["Frontend UI Framework", "React", "19.2.8", "Modern UI component architecture utilizing React.lazy, Suspense, and functional hooks"],
        ["Language Typing", "TypeScript", "6.0.2", "Static type safety ensuring exact alignment between frontend types and backend schemas"],
        ["Build Tool & Bundler", "Vite", "8.3.1", "Next-generation ESM frontend bundler providing HMR and code-split production builds"],
        ["Styling & Theme", "Tailwind CSS", "3.4.17", "Utility-first CSS framework configured with a custom control-room dark color palette"],
        ["Client Data Fetching", "TanStack React Query", "5.104.0", "Asynchronous state management with 2-minute caching, background refetching, and mutations"],
        ["Geospatial Mapping", "Leaflet & React Leaflet", "1.9.4 / 5.0.0", "Interactive hardware-accelerated GIS mapping rendering Indian nodes and transit corridors"],
        ["Data Visualizations", "Recharts", "3.10.1", "Responsive SVG/Canvas charting library for multi-horizon forecasts and comparative bars"],
        ["HTTP Client", "Axios", "1.20.0", "Promise-based HTTP client interfacing with FastAPI backend across all 16 endpoints"],
        ["UI Iconography", "Lucide React", "1.48.0", "Clean, consistent SVG icon system tailored for enterprise dashboards"],
        ["Frontend Testing", "Vitest & Testing Library", "5.0.2 / 16.3.3", "Vite-native unit and component test runner executing 10 verified tests"]
    ]

    add_custom_table(
        doc,
        headers=stack_headers,
        data=stack_data,
        col_widths=[Inches(1.2), Inches(1.5), Inches(1.3), Inches(2.5)],
        alignment=['L', 'L', 'L', 'L'],
        title="Table 5.1 — Verified Production Technology Stack & Library Versions"
    )

    add_heading_2(doc, "5.2 Architectural Rationale for Selected Tooling")
    add_paragraph(
        doc,
        "Every component in the technology stack was selected to satisfy stringent engineering criteria:\n"
        "• FastAPI over Flask/Django: FastAPI provides native async execution, automatic OpenAPI/Swagger documentation generation, "
        "and Pydantic v2 data validation that executes up to 5x faster than traditional Python web frameworks.\n"
        "• Google OR-Tools GLOP over PuLP/SciPy: Google OR-Tools GLOP solver is written in highly optimized C++ with Python bindings. "
        "It solves the 530-variable multi-echelon network problem in ~11 milliseconds, whereas pure Python solvers take seconds.\n"
        "• React 19 + TanStack Query over Redux: Eliminates thousands of lines of boilerplate reducer code while providing automated background "
        "data synchronization, cache invalidation, and seamless optimistic UI updates.\n"
        "• NetworkX over Raw Adjacency Matrices: Enables immediate calculation of complex graph-theoretic metrics (betweenness centrality, "
        "shortest simple detours, and transitive downstream reachability) through clean, expressive Python APIs."
    )

    doc.add_page_break()


def build_chapter_6(doc):
    """Builds Chapter 6: Data Sources & Comprehensive Data Pipeline."""
    add_heading_1(doc, "6. Data Sources & Comprehensive Data Pipeline")

    add_heading_2(doc, "6.1 Hybrid Data Strategy & Provenance Matrix")
    add_paragraph(
        doc,
        "Because real-world enterprise supply chain data is highly confidential and proprietary, NEXUS adopts an academically rigorous "
        "**Hybrid Data Strategy**. We combine real-world empirical time-series distributions with a validated synthetic Indian digital twin network. "
        "The provenance of all data in NEXUS is strictly classified below:"
    )

    prov_headers = ["Dataset / Source", "Classification", "Source / Reference", "Volume / Dimensions", "Specific Purpose in NEXUS"]
    prov_data = [
        ["Walmart Store Sales", "Real / Public Data", "Kaggle Research / Walmart Global Analytics", "421,570 weekly records (45 stores, 81 depts)", "Tuning and evaluating demand forecasting models (XGBoost vs. Baselines)"],
        ["DataCo Global Logistics", "Real / Public Data", "Mendeley Data / Constante et al. (CC BY 4.0)", "35,000+ representative order shipments", "Extracting delivery delay distributions, transit variability, and supplier risk features"],
        ["Indian Hubs Geodesy", "Derived / Spatial Data", "Survey of India / Canonical Logistics Clusters", "30 canonical industrial hubs (Lat, Lon)", "Establishing geodesic distance matrices and highway transit corridors"],
        ["Digital Twin Network", "Simulated Digital Twin", "Synthetic calibrated generator (`network_builder.py`)", "83 nodes, 160 corridors, 500 SKUs, 50k orders", "Providing multi-echelon network topology and inventory stock balances"],
        ["Operational Disruption Shocks", "Scenario Data", "Simulated stress injector (`scenario_engine.py`)", "5 distinct disruption shock types (500 events)", "Stress testing impact propagation, simulation cloning, and OR-Tools optimization"]
    ]

    add_custom_table(
        doc,
        headers=prov_headers,
        data=prov_data,
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.5), Inches(1.2), Inches(1.5)],
        alignment=['L', 'L', 'L', 'L', 'L'],
        title="Table 6.1 — Data Provenance Classification & Source Foundation Matrix"
    )

    add_heading_2(doc, "6.2 Dataset 1: Walmart Store Sales Time-Series")
    add_paragraph(
        doc,
        "The Walmart Store Sales dataset (421,570 historical records spanning February 2010 to October 2012) provides authentic retail sales velocity, "
        "calendar seasonality, holiday surges, and promotional markdown volatility. In NEXUS, store departments are mapped to product catalog SKUs, "
        "and retail stores are mapped to regional consumption demand zones. The genuine variance in this dataset ensures that demand forecasting models "
        "are evaluated on real consumer purchasing volatility rather than artificially smooth synthetic curves."
    )

    add_heading_2(doc, "6.3 Dataset 2: DataCo Global Logistics Supply Chain")
    add_paragraph(
        doc,
        "The DataCo Global Logistics dataset (35,000 representative records) captures end-to-end shipment records, tracking actual shipping days versus "
        "scheduled shipping days, late delivery risk flags, delivery status classifications, order item quantities, and shipping modes. NEXUS extracts "
        "empirical delivery variance patterns (where actual transit days exceed scheduled SLAs) to calibrate realistic supplier on-time delivery rates, "
        "quality defect rates, and lead-time volatility distributions."
    )

    add_heading_2(doc, "6.4 Ingestion, Cleaning & Feature Engineering Pipeline")
    add_paragraph(
        doc,
        "The NEXUS data pipeline (`pipeline/`) executes a multi-stage transformation sequence:\n"
        "1. Ingestion (`data_ingestion.py`): Parses raw CSV records, validates field schemas, and seeds relational tables.\n"
        "2. Cleaning & Normalization (`data_preprocessing.py`): Imputes missing values, enforces positive physical constraints (capacity > 0, unit cost > 0), "
        "and formats timestamps into standardized ISO-8601 strings.\n"
        "3. Autoregressive Feature Engineering (`feature_engineering.py`): Constructs 14 time-series features for demand forecasting:\n"
        "   - Calendar Features: Month, ISO week, quarter, day of year, deterministic trend index.\n"
        "   - Autoregressive Lags: $y_{t-1}, y_{t-2}, y_{t-4}, y_{t-8}$.\n"
        "   - Rolling Window Statistics: 4-week mean, 4-week standard deviation, 8-week mean, 4-week maximum, 4-week minimum.\n"
        "   - Zero Lookahead Bias: All rolling window statistics are explicitly lagged by 1 period ($\text{shift}(1)$) to guarantee no future data leakage."
    )

    doc.add_page_break()
