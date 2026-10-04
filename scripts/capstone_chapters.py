"""
NEXUS Capstone Phase-I Report - Chapters 1 to 3
Detailed academic content for Project Description, Related Work, and Requirement Artifacts.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from scripts.build_full_capstone_report import (
    add_para, add_bullet, add_numbered_item, add_subitem,
    add_chapter_heading, add_section_heading, add_subsection_heading,
    set_cell_background, set_cell_margins, set_table_borders,
    COLOR_BLACK, COLOR_RED, HEX_LIGHT_GRAY
)


def build_chapter_1(doc):
    add_chapter_heading(doc, "1", "PROJECT DESCRIPTION AND OUTLINE")

    add_section_heading(doc, "1.1", "INTRODUCTION")
    p1 = (
        "Global and national supply chain networks are complex, multi-echelon systems responsible for orchestrating "
        "the flow of goods, capital, and information from primary raw material suppliers to end-consumers. Modern enterprises "
        "rely on finely tuned, 'just-in-time' procurement and fulfillment operations across multi-tiered supplier tiers, "
        "manufacturing plants, central fulfillment warehouses, and regional distribution feeder hubs. However, the inherent "
        "interdependence of modern supply chains makes them exceptionally vulnerable to disruptions. Recent macroeconomic "
        "shocks—ranging from global pandemics and geopolitical route closures to extreme climate disruptions, regional monsoon "
        "flooding, and unexpected industrial labor strikes—have repeatedly exposed the systemic brittleness of traditional "
        "logistics networks."
    )
    add_para(doc, p1)

    p2 = (
        "This project proposes a transformative engineering solution to these supply chain challenges through the design and "
        "implementation of NEXUS — an AI-Powered Supply Chain Intelligence, Predictive Risk Management, and Multi-Echelon "
        "Linear Optimization Platform. NEXUS models an authentic national digital twin network across India, capturing 83 critical "
        "logistics nodes and 160 multimodal transit corridors. Rather than operating as a passive analytics reporting dashboard, "
        "NEXUS implements a closed-loop decision workflow: Monitor → Predict → Analyze Impact → Simulate → Optimize → Recommend. "
        "By fusing empirical time-series demand data (Walmart Store Sales dataset with 421,570 records) and global fulfillment risk "
        "telemetry (DataCo Logistics dataset with 35,000 records) with advanced machine learning and Google OR-Tools mathematical "
        "programming, NEXUS empowers enterprise supply chain managers to anticipate disruptions before they cascade, conduct "
        "non-destructive 'what-if' shock simulations, and autonomously compute cost-optimal reallocation strategies in real time."
    )
    add_para(doc, p2)

    add_section_heading(doc, "1.2", "MOTIVATION FOR THE WORK")
    p3 = (
        "The primary motivation behind this project is to eliminate the severe operational latency, financial waste, and "
        "decision paralysis that afflict enterprise supply chains during unforeseen disruptions. In contemporary industry "
        "settings, enterprise resource planning (ERP) systems operate almost exclusively on historical batch transactions. When a "
        "primary supplier abruptly cuts production or an interstate transit highway is severed, supply chain planners are overwhelmed "
        "by fragmented data across siloed spreadsheets and static dashboards. Human planners, constrained by cognitive limits, "
        "invariably resort to rigid, localized heuristics—such as blind spot-market purchasing, ad-hoc expedited air freight, or "
        "simply rationing inventory. These uncoordinated actions severely trigger the notorious 'Bullwhip Effect', amplifying order "
        "volatility up the supply chain, inflating emergency logistics costs, and resulting in millions of rupees in unmet stockout penalties."
    )
    add_para(doc, p3)

    p4 = (
        "Furthermore, existing commercial supply chain software packages fail to bridge the critical gap between predictive "
        "machine learning and prescriptive linear optimization. While modern data science teams may deploy accurate time-series "
        "demand forecasting algorithms, the resulting forecast numbers are rarely ingested into mathematical solvers that respect "
        "production capacity ceilings, warehouse throughput thresholds, and multi-tier route conservation laws. NEXUS addresses "
        "this fundamental engineering void by creating an integrated, closed-loop decision platform. The motivation is to provide "
        "logistics directors with an intelligent 'Control Room' that continuously computes optimal dispatches, preserves customer "
        "service levels at 100%, and proves substantial empirical cost savings under extreme operational shocks."
    )
    add_para(doc, p4)

    add_section_heading(doc, "1.3", "PROBLEM STATEMENT")
    p5 = (
        "Modern multi-echelon enterprise supply chains face multi-dimensional operational vulnerabilities that severely "
        "undermine delivery reliability, operational cost efficiency, and customer satisfaction. The core problems can be "
        "formally delineated across four major engineering deficiencies:"
    )
    add_para(doc, p5)

    add_bullet(doc, "Lack of Multi-Tier Upstream Visibility:", 
               "Most logistics managers maintain direct visibility only into Tier-1 suppliers. A disruption at a secondary raw material vendor or feeder distribution hub remains invisible until delivery deadlines are catastrophically breached, leaving zero lead time for preventive intervention.")
    add_bullet(doc, "Disconnection Between Prediction and Prescription:", 
               "Conventional analytics platforms operate either purely descriptively (retrospective BI dashboards) or in isolated prediction (forecasting algorithms outputting numbers into CSVs). There is no automated algorithmic pipeline that maps high disruption probabilities directly into optimal rerouting dispatches.")
    add_bullet(doc, "Absence of Non-Destructive Scenario Testing:", 
               "Supply chain planners have no reliable digital sandbox to stress-test their networks against hypothetical shocks—such as an 80% capacity cut on a key industrial vendor, route blockades, or a 70% regional demand surge—without risking corruption of production databases.")
    add_bullet(doc, "Catastrophic Penalty Costs from Uncoordinated Heuristics:", 
               "Under un-optimized manual response strategies, supply disruptions rapidly cause downstream stockouts, resulting in exorbitant contractual SLA penalties, loss of brand equity, and customer churn.")

    p6 = (
        "To resolve these interconnected problems, there is an urgent need to design, engineer, and deploy an end-to-end "
        "decision intelligence platform that unites predictive machine learning, graph-based failure propagation, and mathematical "
        "multi-echelon optimization into a unified, high-performance web architecture."
    )
    add_para(doc, p6)

    add_section_heading(doc, "1.4", "OBJECTIVE OF THE WORK")
    p7 = (
        "The primary objective of this project is to architect, develop, empirically benchmark, and deploy NEXUS — an enterprise-grade "
        "decision-intelligence platform for multi-echelon supply chain risk prediction and linear optimization. The specific "
        "measurable objectives of the capstone project are as follows:"
    )
    add_para(doc, p7)

    add_numbered_item(doc, "1.", "Design and establish an authentic Indian national logistics Digital Twin topology comprising 83 multi-tier facilities (Suppliers, Manufacturing Plants, Central Warehouses, Feeder Hubs, and Demand Zones) interconnected via 160 realistic multimodal transit corridors with calibrated geodesic and highway distances.")
    add_numbered_item(doc, "2.", "Ingest, clean, and validate empirical enterprise supply chain datasets, incorporating 421,570 weekly historical records from the Walmart Store Sales Forecasting dataset and 35,000 shipment variance records from the DataCo Global Supply Chain dataset.")
    add_numbered_item(doc, "3.", "Develop, tune, and evaluate machine learning models for supply chain intelligence, including multi-step recursive XGBoost demand regressors benchmarked against naive and moving average baselines, supervised XGBoost supplier disruption risk classifiers evaluated on strictly unseen out-of-sample vendor cohorts, and unsupervised Isolation Forest transaction anomaly detectors.")
    add_numbered_item(doc, "4.", "Formulate and implement a NetworkX directed graph impact propagation algorithm to traverse supply dependencies downstream, calculate multi-tier inventory runways, and identify vulnerable facilities prior to stockout occurrence.")
    add_numbered_item(doc, "5.", "Engineer an in-memory, copy-on-write scenario simulation engine capable of modeling 5 distinct operational disruption archetypes (Supplier Failure, Route Severance, Demand Surge, Facility Shutdown, and Compound Shocks) without mutating persistent relational storage.")
    add_numbered_item(doc, "6.", "Formulate and solve a multi-echelon mixed-integer linear programming (MILP) model using Google OR-Tools (GLOP) to minimize total operational expenditure across procurement, transportation, holding, shortage penalties, and risk penalties, benchmarking the solution against un-optimized baseline heuristics.")
    add_numbered_item(doc, "7.", "Deploy an asynchronous, production-grade FastAPI REST backend exposing 16 endpoints with OpenAPI 3.1 documentation, coupled with an ultra-responsive React 19 control-room web application featuring interactive Leaflet GIS visualization, Recharts data analytics, and plain-language executive recommendation synthesis.")

    add_section_heading(doc, "1.5", "SUMMARY")
    p8 = (
        "Chapter 1 has articulated the foundational engineering context, operational motivations, formal problem statements, "
        "and specific measurable objectives of the NEXUS platform. By transitioning from retrospective descriptive reporting "
        "to a continuous, closed-loop decision intelligence paradigm, NEXUS addresses critical vulnerabilities in modern multi-echelon "
        "logistics. The remainder of this report investigates related state-of-the-art literature, details system requirement "
        "specifications, outlines architectural design methodologies, presents technical coding solutions, demonstrates empirical "
        "optimization results, and reviews full-scale prototype implementations."
    )
    add_para(doc, p8)
    doc.add_page_break()


def build_chapter_2(doc):
    add_chapter_heading(doc, "2", "RELATED WORK INVESTIGATION")

    add_section_heading(doc, "2.1", "EXISTING APPROACHES/METHODS")
    p1 = (
        "Enterprise supply chain management, predictive risk monitoring, and inventory logistics have been investigated across "
        "industrial engineering and computer science for decades. Existing industry methodologies and academic software tools "
        "can be categorized into six major technological approaches:"
    )
    add_para(doc, p1)

    add_bullet(doc, "1. Enterprise Resource Planning (ERP) Modules (SAP SCM, Oracle SCM, Microsoft Dynamics):", 
               "Traditional ERP systems serve as the core transactional backbone of modern enterprises. They maintain transactional tables for purchase orders, inventory counts, bills of materials (BOM), and ledger accounts. However, standard ERP suites operate as passive transaction recorders rather than autonomous decision engines.")
    add_bullet(doc, "2. Business Intelligence & Descriptive Dashboards (Tableau, Microsoft PowerBI, QlikView):", 
               "Widely adopted across corporate logistics departments to visualize historical Key Performance Indicators (KPIs) such as on-time in-full (OTIF) rates, monthly freight expenditures, and stock turnover ratios. These tools excel at retroactive data slicing and aggregation.")
    add_bullet(doc, "3. Classical Statistical & Univariate Time-Series Forecasting (ARIMA, SARIMA, Exponential Smoothing, Facebook Prophet):", 
               "Widely applied in retail demand forecasting to project future product consumption based on past historical trends and calendar seasonality. These statistical models fit auto-regressive moving averages to individual time series in isolation.")
    add_bullet(doc, "4. Rule-Based Inventory Heuristics (Reorder Point, Safety Stock Buffers, Fixed Vendor Contracts):", 
               "Standard supply chain practice relies on static analytical formulas such as the Economic Order Quantity (EOQ) and continuous-review (s, S) policies. When demand exceeds expectations or lead times fluctuate, safety stock is consumed, and static contractual agreements dictate primary supplier replenishment.")
    add_bullet(doc, "5. Commercial Supply Chain Simulation Software (AnyLogic, Llamasoft Supply Chain Guru, Simio):", 
               "Heavyweight desktop simulation packages utilized by specialized industrial engineering consultants to model discrete-event stochastic agent behavior and physical facility queuing over multi-month planning cycles.")
    add_bullet(doc, "6. Standalone Mathematical Optimization Solvers (CPLEX, Gurobi, Linear Programming Libraries):", 
               "Operations research literature provides extensive formulations for transportation problems, network flow, and facility location optimization. Solvers find the mathematically optimal allocation of flows across cost matrices given rigid supply-demand constraints.")

    add_section_heading(doc, "2.2", "PROS AND CONS OF THE STATED APPROACHES/METHODS")
    p2 = (
        "A rigorous comparative evaluation reveals significant structural gaps in how existing methodologies handle real-time "
        "multi-echelon supply disruptions. Below is an exhaustive technical analysis of their respective strengths and limitations:"
    )
    add_para(doc, p2)

    # Pros and Cons Analysis
    add_para(doc, "1. Enterprise Resource Planning (ERP) Systems:", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Robust data integrity, centralized relational enterprise databases, automated invoicing, standardized accounting, and enterprise-wide access control.")
    add_bullet(doc, "Cons:", "Rigid monolithic architectures, slow batch-processing cycles, absence of native predictive machine learning, high operational complexity, and inability to dynamically reroute freight during acute disruptions.")

    add_para(doc, "2. Business Intelligence (BI) Dashboards:", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Intuitive visual graphs, fast aggregation over historical data lakes, customizable executive reporting views, and cross-departmental KPI transparency.")
    add_bullet(doc, "Cons:", "Entirely retrospective ('rear-view mirror' analytics). Dashboards inform managers that a stockout has already occurred, but cannot predict latent vendor collapse, trace multi-tier graph impacts, or compute optimal mitigation dispatches.")

    add_para(doc, "3. Classical Statistical Time-Series Models (ARIMA / Prophet):", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Statistically sound mathematical foundations, strong performance on linear stationary series, automated confidence intervals, and interpretability.")
    add_bullet(doc, "Cons:", "Extremely vulnerable to non-linear holiday demand shocks and multi-variate promotions; computationally expensive to scale independently across tens of thousands of SKUs; completely decoupled from network capacity constraints.")

    add_para(doc, "4. Rule-Based Heuristic Operations:", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Computationally trivial, zero software overhead, easy for warehouse staff to understand, and operates deterministically under normal steady-state conditions.")
    add_bullet(doc, "Cons:", "Catastrophically fails during systemic shocks. When a primary vendor fails, heuristic binding leaves warehouses completely stranded without exploring alternative multi-echelon suppliers, causing massive shortage penalties.")

    add_para(doc, "5. Commercial Heavyweight Simulation Suites:", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Detailed physical and physics-level modeling, discrete event stochastic queues, and visual 3D simulation.")
    add_bullet(doc, "Cons:", "Prohibitively expensive proprietary licensing, steep learning curve requiring specialized consultants, slow execution times (hours/days), and complete disconnect from operational real-time web control rooms.")

    add_para(doc, "6. Standalone OR Optimization Solvers:", bold=True, space_after=2)
    add_bullet(doc, "Pros:", "Guaranteed global mathematical optimality, precise constraint enforcement, and rapid convergence on linear systems.")
    add_bullet(doc, "Cons:", "Solvers operate in a vacuum. They require manual mathematical formulation and clean parameter input matrices. If parameters (demand projections, risk scores, severed corridors) are not fed dynamically from real-time ML and graph pipelines, the solver is useless to daily operations.")

    p3 = (
        "Summary of the Technological Gap: The existing landscape is fundamentally bifurcated. Enterprise systems either possess "
        "transactional data (ERP/BI) or machine learning models (forecasting) or mathematical programming (operations research), "
        "but zero systems integrate them into a unified, responsive closed-loop platform. NEXUS bridges this gap by directly chaining "
        "empirical data ingestion, predictive machine learning, NetworkX graph impact analysis, non-destructive simulation, and Google "
        "OR-Tools linear optimization into an accessible, real-time web platform."
    )
    add_para(doc, p3, space_before=6)
    doc.add_page_break()


def build_chapter_3(doc):
    add_chapter_heading(doc, "3", "REQUIREMENT ARTIFACTS")

    add_section_heading(doc, "3.1", "INTRODUCTION")
    p1 = (
        "The requirements engineering phase for the NEXUS Supply Chain Intelligence Platform establishes the foundational "
        "specifications necessary to ensure that the system is functionally robust, mathematically accurate, highly performant, "
        "and operationally intuitive. Modern multi-echelon supply chain decision support demands strict adherence to both "
        "computational and operational criteria: the platform must process complex empirical data matrices, execute machine "
        "learning inferences with low latency, solve multi-variable linear programs under 50 milliseconds, and present an ergonomic, "
        "mission-critical control-room interface to executive decision-makers. The requirement artifacts are systematically classified "
        "into hardware/software infrastructure, data specifications, functional capabilities, non-functional performance/security "
        "thresholds, and user experience requirements."
    )
    add_para(doc, p1)

    add_section_heading(doc, "3.2", "HARDWARE AND SOFTWARE REQUIREMENTS")
    p2 = "To support end-to-end data processing, machine learning training, graph traversal, and responsive web rendering, the minimum and recommended system requirements are delineated below:"
    add_para(doc, p2)

    add_para(doc, "Hardware Requirements:", bold=True, space_after=2)
    add_bullet(doc, "Processor (Server / Development):", "Modern Multi-core x86_64 or ARM64 CPU (minimum 4 physical cores, 8 threads; Intel Core i7 11th Gen / AMD Ryzen 7 / Apple M-series or higher) to enable multi-threaded OR-Tools solving and parallel XGBoost tree construction.")
    add_bullet(doc, "System Memory (RAM):", "Minimum 8.0 GB RAM (16.0 GB recommended) to accommodate in-memory caching of the 421k-record Walmart dataset, feature engineering matrices, and copy-on-write simulation state clones.")
    add_bullet(doc, "Storage:", "Minimum 10.0 GB of available solid-state storage (NVMe SSD recommended) to store raw datasets, Parquet data caches, SQLite/PostgreSQL database files, serialized ML models, and compiled frontend production bundles.")
    add_bullet(doc, "Network Interface:", "Standard TCP/IP Ethernet or high-speed Wi-Fi connection for local REST API communication (localhost loopback) and external mapping tile retrieval.")
    add_bullet(doc, "Client Display:", "Minimum 1366x768 display resolution (1920x1080 Full HD recommended) for multi-column control-room layout and high-density Leaflet GIS map rendering.")

    add_para(doc, "Software Requirements:", bold=True, space_after=2, space_before=4)
    add_bullet(doc, "Operating System:", "Cross-platform compatibility: Microsoft Windows 10/11 (64-bit), Ubuntu Linux 22.04 LTS+, or macOS Ventura/Sonoma.")
    add_bullet(doc, "Backend Runtime & Core Libraries:", "Python 3.11+ / Python 3.13; FastAPI 0.115+, Uvicorn (ASGI server), Pydantic v2 (data validation contracts), SQLAlchemy 2.0 (ORM database engine).")
    add_bullet(doc, "Scientific Computing & Machine Learning:", "Scikit-Learn 1.7.0, XGBoost 3.4.1, Joblib, NumPy 2.3.1, Pandas 2.3.1, SciPy 1.18.1.")
    add_bullet(doc, "Graph Theory & Mathematical Optimization:", "NetworkX 3.6.1 (graph modeling and centrality algorithms), Google OR-Tools 9.15+ (Linear Solver GLOP).")
    add_bullet(doc, "Geospatial GIS Engine:", "GeoPandas 1.1.4, Shapely 2.1.2, PyProj 3.8.0.")
    add_bullet(doc, "Database Systems:", "Standalone SQLite engine (`data/nexus.db`, 12.8 MB) with native zero-friction execution, fully compatible with enterprise PostgreSQL 15+.")
    add_bullet(doc, "Frontend Web Technologies:", "Node.js 18.0+, React 19.2+, TypeScript 6.0+, Vite 8.3+, Tailwind CSS 3.4.17, TanStack React Query v5, Recharts 3.10+, React Leaflet 4.2+, Axios 1.20+, Lucide React.")
    add_bullet(doc, "Testing & Quality Verification Frameworks:", "Pytest 9.1.1 (backend test suite), Vitest & React Testing Library (frontend test suite).")
    add_bullet(doc, "Integrated Development Environments (IDE):", "Visual Studio Code (VS Code) with Python, ESLint, Tailwind CSS IntelliSense, and Git extensions.")

    add_section_heading(doc, "3.3", "SPECIFIC PROJECT REQUIREMENTS")

    add_subsection_heading(doc, "3.3.1", "Data Requirements")
    add_bullet(doc, "Empirical Demand Historical Corpus:", "The platform must ingest and validate 421,570 weekly historical retail records from the Walmart Store Sales dataset, maintaining data integrity across store IDs, department numbers, weekly sales, and holiday indicators.")
    add_bullet(doc, "Logistics & Risk Variance Logs:", "The platform must process 35,000 shipment variance records from the DataCo Global Supply Chain dataset to model realistic delivery lead-time standard deviations, delay frequencies, and material quality rates.")
    add_bullet(doc, "Digital Twin Relational Entities:", "The database must store and maintain relationships across 14 tables: `suppliers` (20), `products` (50), `production_units` (8), `warehouses` (10), `distribution_hubs` (15), `inventory` (500), `demand_zones` (30), `routes` (160), `orders` (50,000), `disruptions`, `risk_events`, `forecasts`, `optimization_runs`, and `recommendations`.")
    add_bullet(doc, "Geospatial Coordinates:", "Every facility node must possess verified decimal latitude/longitude coordinates across major Indian commercial hubs (e.g., Delhi NCR, Mumbai MMR, Bengaluru, Chennai, Kolkata, Ahmedabad) along with road transit distances calibrated by a 1.22x highway tortuosity factor.")

    add_subsection_heading(doc, "3.3.2", "Functionality Requirements")
    add_bullet(doc, "Automated Pipeline Seeding:", "A single command (`python run_pipeline.py`) must ingest data, seed the database, train ML models, compute baseline metrics, execute shock simulations, solve optimizations, and generate executive reports.")
    add_bullet(doc, "Multi-Step Demand Forecasting:", "The forecasting engine must generate 4-week to 12-week recursive demand projections, computing MAE, RMSE, and sMAPE against naive and moving average baselines.")
    add_bullet(doc, "Out-of-Sample Supplier Risk Classification:", "The risk engine must predict vendor failure probability using supervised classification evaluated on strictly held-out vendor cohorts.")
    add_bullet(doc, "Unsupervised Anomaly Detection:", "The system must scan incoming order volumes and freight transit delays using an Isolation Forest to flag operational anomalies exceeding 2.5 standard deviations.")
    add_bullet(doc, "Graph Failure Propagation:", "The impact engine must traverse NetworkX directed dependency trees to calculate remaining inventory runway days and project downstream service level drops.")
    add_bullet(doc, "Non-Destructive Scenario Simulation:", "Users must be able to inject 5 distinct disruption shocks (Supplier Failure, Route Severance, Demand Surge, Warehouse Shutdown, Combined) in an in-memory clone without altering production data.")
    add_bullet(doc, "Mathematical Optimization Solver:", "The optimization engine must formulate and solve a multi-echelon linear program using Google OR-Tools GLOP to eliminate shortages and minimize total operational cost.")
    add_bullet(doc, "Explainable Decision Synthesis:", "The recommendation engine must translate mathematical decision variable vectors into plain-language executive directives with quantified financial savings.")

    add_subsection_heading(doc, "3.3.3", "Performance Requirements")
    add_bullet(doc, "API Response Latency:", "Entity lookups must return in < 50ms; ML inference in < 250ms; and OR-Tools optimization in < 50ms.")
    add_bullet(doc, "Solver Efficiency:", "The Google OR-Tools GLOP linear solver must solve the 530-variable multi-echelon network problem in under 0.05 seconds.")
    add_bullet(doc, "Frontend Bundle Footprint:", "The initial production JavaScript bundle shell must not exceed 400 kB gzipped, utilizing `React.lazy` code splitting for mapping and charting libraries.")
    add_bullet(doc, "Concurrent Data Handling:", "The database engine must handle concurrent read requests from the 8 dashboard screens without table locking or connection pool exhaustion.")

    add_subsection_heading(doc, "3.3.4", "Security Requirements")
    add_bullet(doc, "Schema Validation & Injection Defense:", "All incoming API request payloads must be strictly validated using Pydantic v2 schemas to eliminate SQL injection, type coercion errors, and buffer overflows.")
    add_bullet(doc, "Defensive Environment Configuration:", "Sensitive configuration parameters (database URIs, host ports, risk threshold penalties) must be isolated in `.env` files and managed via Pydantic BaseSettings.")
    add_bullet(doc, "CORS Middleware:", "FastAPI backend must implement strict Cross-Origin Resource Sharing (CORS) middleware, permitting only authorized origins.")

    add_subsection_heading(doc, "3.3.5", "Looks and Feel Requirements")
    add_bullet(doc, "Enterprise Control-Room Aesthetics:", "The UI must employ a dark-themed palette (`nexus-950` #0B0F19 to `nexus-700` #334155) engineered for low-fatigue operations in 24/7 logistics centers.")
    add_bullet(doc, "Status & Risk Color Signifiers:", "Critical metrics must use standardized semantic color coding: Green (Low Risk / Optimal), Amber (Moderate Risk / Warning), Red (High Risk / Disrupted), and Purple (Mathematical Optimization).")
    add_bullet(doc, "Interactive Geospatial Mapping:", "The GIS map must render facility nodes with customized SVG markers, color-coded by tier, and draw interactive polyline freight corridors with popup metrics.")
    add_bullet(doc, "Responsive Layout:", "The dashboard must adapt seamlessly to high-resolution multi-monitor control centers as well as standard laptop displays.")

    add_section_heading(doc, "3.4", "SUMMARY")
    p3 = (
        "Chapter 3 has defined the complete requirement artifacts for the NEXUS platform. Meeting these hardware, software, "
        "data, functional, performance, security, and usability specifications guarantees an industrial-strength foundation for "
        "multi-echelon supply chain intelligence. The next chapter presents the design methodology and architectural innovation "
        "underpinning the system."
    )
    add_para(doc, p3)
    doc.add_page_break()


print("Chapters 1 to 3 loaded.")
