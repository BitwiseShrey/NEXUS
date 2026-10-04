"""
NEXUS Report Generator - Part 2:
- Chapter 7: Database Design & Relational Data Model
- Chapter 8: Digital Supply Chain Twin (Indian Logistics Network)
- Chapter 9: Demand Forecasting Engine
- Chapter 10: Supervised Supplier Risk Prediction Engine
- Chapter 11: Operational Anomaly Detection Engine
- Chapter 12: Cascading Impact Propagation Analysis
- Chapter 13: Scenario Simulation Studio
"""

import os
from docx.shared import Inches, Pt, RGBColor
from scripts.doc_builder_helpers import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_callout,
    add_image_with_caption, add_custom_table, add_equation_block,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DARK_SLATE, COLOR_MUTED, COLOR_BODY
)


def build_chapter_7(doc):
    """Builds Chapter 7: Database Design & Relational Data Model."""
    add_heading_1(doc, "7. Relational Database Design")

    add_heading_2(doc, "7.1 Database Architecture & Session Management")
    add_paragraph(
        doc,
        "The persistence layer of NEXUS is built on **SQLAlchemy 2.0 ORM**, configured with a flexible multi-database abstraction layer. "
        "In development and demonstration environments, the system operates on a zero-friction, standalone **SQLite 3** database located at "
        "`data/nexus.db` (12.8 MB). The database layer is architected with complete PostgreSQL DDL compatibility: in production cloud deployments, "
        "the database engine seamlessly connects to an enterprise PostgreSQL instance via the `DATABASE_URL` environment variable."
    )
    add_paragraph(
        doc,
        "Database sessions are managed using SQLAlchemy's scoped `sessionmaker` pattern with automatic connection pooling, transaction isolation, "
        "and clean session closure upon request completion. The database contains 14 relational tables mapping the physical entities, operational flows, "
        "predictive telemetry, and optimization audit runs."
    )

    add_heading_2(doc, "7.2 Complete 14-Table Relational Schema Catalog")
    add_paragraph(
        doc,
        "The table below documents the verified schema and actual record counts extracted directly from the live `data/nexus.db` database:",
        bold_prefix="Verified Database Inventory:"
    )

    db_headers = ["Table Name", "SQLAlchemy Model", "Primary Key", "Foreign Keys & Key Relationships", "Verified Row Count", "Table Functional Description"]
    db_data = [
        ["suppliers", "Supplier", "supplier_id (VARCHAR 50)", "Indexed on risk_score and status", "20 rows", "Tier-1 and Tier-2 component vendors, capacities, lead times, and risk scores"],
        ["products", "Product", "product_id (VARCHAR 50)", "FK: primary_supplier_id → suppliers.supplier_id", "50 rows", "Catalog finished SKUs and subassemblies with unit costs and criticality tiers (1-3)"],
        ["production_units", "ProductionUnit", "production_id (VARCHAR 50)", "Geocoded coordinates across Indian clusters", "8 rows", "Manufacturing and final assembly facilities with daily throughput capacities"],
        ["warehouses", "Warehouse", "warehouse_id (VARCHAR 50)", "Relational linkage to Inventory table", "10 rows", "Central fulfillment distribution centers tracking capacity and utilization"],
        ["distribution_hubs", "DistributionHub", "hub_id (VARCHAR 50)", "Geocoded sorting hubs", "15 rows", "Regional intermediate cross-dock terminals and sorting points"],
        ["inventory", "Inventory", "inventory_id (INTEGER Auto)", "FK: warehouse_id, product_id", "500 rows", "Stock on hand, reserved units, safety stock, reorder point, and stockout risk"],
        ["demand_zones", "DemandZone", "zone_id (VARCHAR 50)", "FK: product_id → products.product_id", "30 rows", "Urban consumer consuming markets across North, South, West, East, Central"],
        ["routes", "Route", "route_id (VARCHAR 50)", "Indexed on origin and destination", "160 rows", "Multimodal freight transit corridors (Road, Rail, Air) with highway distance & cost"],
        ["orders", "Order", "order_id (VARCHAR 50)", "FK: product_id → products.product_id", "50,000 rows", "Historical transaction logs tracking expected vs actual delivery and SLA status"],
        ["disruptions", "Disruption", "disruption_id (VARCHAR 50)", "FK: affected_supplier, warehouse, route", "500 rows", "Historical and simulated disruption incidents, severities, and durations"],
        ["optimization_runs", "OptimizationRun", "run_id (VARCHAR 50)", "Audit linkage to Recommendations", "30 rows", "Google OR-Tools solver execution outputs, costs, shortages, and service levels"],
        ["recommendations", "Recommendation", "recommendation_id (VARCHAR 50)", "FK: run_id → optimization_runs.run_id", "30 rows", "Actionable executive mitigation briefs, ROI savings, and Plan Robustness Index"],
        ["forecasts", "Forecast", "forecast_id (VARCHAR 50)", "Target product_id, horizon, JSON metrics", "17 rows", "Stored demand forecasting runs, predicted demand vectors, and MAE/RMSE"],
        ["risk_events", "RiskEvent", "event_id (VARCHAR 50)", "Audit table for real-time risk breaches", "0 rows (Runtime)", "Dynamic event ledger populated when operational risk thresholds are breached"]
    ]

    add_custom_table(
        doc,
        headers=db_headers,
        data=db_data,
        col_widths=[Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.3), Inches(0.8), Inches(1.0)],
        alignment=['L', 'L', 'L', 'L', 'C', 'L'],
        title="Table 7.1 — Complete Relational Database Model Catalog & Row Counts"
    )

    add_heading_2(doc, "7.3 Entity-Relationship Topology")
    add_paragraph(
        doc,
        "The relational schema enforces strict referential integrity. Suppliers provide components for Products, which are stocked as line items "
        "in the Inventory table at specific Warehouses. Warehouses dispatch goods to regional Distribution Hubs and Demand Zones via multimodal Routes. "
        "When an optimization run completes, the resulting mathematical vectors and plain-language executive directives are linked via `run_id` "
        "between the `optimization_runs` and `recommendations` tables:"
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/13_database_er_diagram.png",
        "Figure 7.1 — Relational Database Schema & Entity Relationships (14 Models with Referential Foreign Keys)",
        width=Inches(5.4)
    )

    doc.add_page_break()


def build_chapter_8(doc):
    """Builds Chapter 8: Digital Supply Chain Twin."""
    add_heading_1(doc, "8. Digital Supply Chain Twin (Indian Network)")

    add_heading_2(doc, "8.1 Concept of the Calibrated Digital Twin")
    add_paragraph(
        doc,
        "In modern systems engineering, a **Digital Supply Chain Twin** is a dynamic, software-based representation of the physical supply network. "
        "Rather than treating a supply chain as an abstract balance sheet, NEXUS grounds the digital twin in authentic geography, physical throughput "
        "constraints, multimodal transport physics, and multi-tier bills of materials."
    )
    add_paragraph(
        doc,
        "Because proprietary factory floor telemetry is legally confidential, NEXUS generates a calibrated digital twin topology that strictly replicates "
        "the statistical properties of Indian industrial commerce. The network models **83 distinct physical facility nodes** connected by **160 active "
        "transit corridors**, providing an authentic testbed for multi-echelon failure propagation and optimization."
    )

    add_heading_2(doc, "8.2 Geodesic Coordinates & Indian Industrial Hubs")
    add_paragraph(
        doc,
        "The digital twin geocodes all 83 facilities across **30 canonical Indian industrial and logistics clusters** (`digital_twin/geo_engine.py`). "
        "The geographic distribution spans all major industrial belts of India:"
    )

    hub_headers = ["Macro-Region", "Canonical Industrial Hub", "Geographic Coordinates", "Industrial Specialization"]
    hub_data = [
        ["Northern Belt", "Delhi NCR (Gurgaon / Okhla)", "28.6139° N, 77.2090° E", "Automotive components, consumer electronics, e-commerce fulfillment"],
        ["Northern Belt", "Jaipur (Sitapura / VKI)", "26.9124° N, 75.7873° E", "Industrial machinery, textiles, precision casting"],
        ["Northern Belt", "Pantnagar (SIDCUL)", "29.0222° N, 79.4897° E", "Automotive OEMs, FMCG, heavy engineering"],
        ["Northern Belt", "Ludhiana (Industrial Area)", "30.9010° N, 75.8573° E", "Fasteners, metal hardware, industrial tooling"],
        ["Western Belt", "Pune (Chakan / Bhosari)", "18.7606° N, 73.8617° E", "Automotive Tier-1 precision assemblies, heavy tooling, electronics"],
        ["Western Belt", "Mumbai (Bhiwandi Logistic Hub)", "19.2967° N, 73.0628° E", "Western mega-warehousing, port container de-stuffing, FMCG"],
        ["Western Belt", "Ahmedabad / Sanand (Aslali)", "22.9228° N, 72.5855° E", "Chemicals, automotive manufacturing, polymer casting"],
        ["Western Belt", "Surat (Pandesara / Sachin)", "21.1702° N, 72.8311° E", "Synthetic textiles, precision industrial packaging"],
        ["Southern Belt", "Bengaluru (Hoskote / Peenya)", "13.0712° N, 77.7981° E", "Embedded hardware, electronics manufacturing, aerospace"],
        ["Southern Belt", "Chennai (Sri City / Sriperumbudur)", "13.5284° N, 80.0270° E", "Automotive manufacturing, consumer electronics assembly"],
        ["Southern Belt", "Hyderabad (Medchal / Patancheru)", "17.6297° N, 78.4814° E", "Pharmaceutical packaging, precision engineering, chemicals"],
        ["Eastern Belt", "Kolkata (Dankuni Logistics Park)", "22.6841° N, 88.2917° E", "Eastern distribution hub, riverine port logistics, FMCG"],
        ["Eastern Belt", "Jamshedpur (Adityapur)", "22.8046° N, 86.2029° E", "Raw steel production, heavy forgings, industrial casting"],
        ["Central Belt", "Nagpur (MIHAN Logistic Zone)", "21.1458° N, 79.0882° E", "Central multimodal transit consolidation, cold chain logistics"],
        ["Central Belt", "Indore (Pithampur)", "22.6145° N, 75.6917° E", "Heavy machinery, automotive components, pharmaceutical formulation"]
    ]

    add_custom_table(
        doc,
        headers=hub_headers,
        data=hub_data,
        col_widths=[Inches(1.2), Inches(1.8), Inches(1.5), Inches(2.0)],
        alignment=['L', 'L', 'C', 'L'],
        title="Table 8.1 — Canonical Indian Logistics Hubs Geocoded Coordinates"
    )

    add_heading_2(doc, "8.3 Road Network Mathematics & Highway Tortuosity")
    add_paragraph(
        doc,
        "In simplistic academic models, transit distances are frequently calculated as Euclidean straight lines. In real-world Indian logistics, "
        "terrain obstacles, ghat passes, and highway bypasses introduce substantial winding factors. The NEXUS Geospatial Engine (`GeoEngine`) "
        "computes realistic transit distances and durations through rigorous geodesic mathematics:"
    )

    add_equation_block(
        doc,
        "d_{hav} = 2 R \\arcsin \\left( \\sqrt{\\sin^2\\left(\\frac{\\Delta \\phi}{2}\\right) + \\cos(\\phi_1) \\cos(\\phi_2) \\sin^2\\left(\\frac{\\Delta \\lambda}{2}\\right)} \\right)",
        eq_num="Eq. 8.1",
        explanation="Haversine great-circle distance formula where R = 6,371.0 km (Earth radius), phi represents latitude, and lambda represents longitude."
    )

    add_paragraph(
        doc,
        "To convert great-circle distance $d_{hav}$ into commercial highway kilometers, NEXUS introduces an empirical **Indian National Highway Tortuosity Factor** "
        "of $\\tau = 1.22$. Furthermore, commercial transit durations are parameterized on empirical freight speeds:"
    )

    add_equation_block(
        doc,
        "d_{road} = \\max(1.22 \\cdot d_{hav}, 15.0\\text{ km}), \\qquad T_{transit} = \\begin{cases} \\max\\left(\\frac{d_{road}}{400\\text{ km/day}}, 0.5\\right) & \\text{if ROAD} \\\\ \\max\\left(\\frac{d_{road}}{550\\text{ km/day}}, 1.0\\right) & \\text{if RAIL} \\\\ 1.0\\text{ day} & \\text{if AIR} \\end{cases}",
        eq_num="Eq. 8.2",
        explanation="Highway road distance and commercial freight transit durations assuming 40 km/h average speed across a 10-hour daily driving window for road logistics."
    )

    add_heading_2(doc, "8.4 Multi-Echelon Network Topology Breakdown")
    add_paragraph(
        doc,
        "The digital twin models five multi-echelon tiers with explicit physical capacities:\n"
        "• 20 Suppliers: 12 Tier-1 precision component vendors (capacities 8,000 - 15,000 units/mo) and 8 Tier-2 raw material vendors (capacities 12,000 - 30,000 units/mo).\n"
        "• 8 Production Units: Manufacturing and assembly plants located in Sanand, Pune, Gurgaon, Sriperumbudur, Hoskote, Medchal, Pantnagar, and Pithampur.\n"
        "• 10 Central Warehouses: Regional hubs (Bhiwandi, Dankuni, Nagpur MIHAN, Gurgaon, Hoskote, Sri City, Aslali, Jaipur, Lucknow, Kolkata) with storage capacities up to 100,000 units.\n"
        "• 15 Distribution Feeder Hubs: Cross-dock sorting hubs consolidating freight for retail markets.\n"
        "• 30 Demand Zones: Metropolitan consumer clusters across North, West, South, East, and Central zones with monthly demand up to 5,000 units per SKU.\n"
        "• 160 Multimodal Corridors: 120 Road corridors, 30 Rail freight corridors, and 10 Air express corridors."
    )

    add_heading_2(doc, "8.5 Inventory Mechanics: Safety Stock & Reorder Points")
    add_paragraph(
        doc,
        "The Inventory model (`backend/app/models/orm_models.py`) tracks 500 distinct facility-SKU combinations. For every inventory record, "
        "reorder points and safety stocks are calculated to buffer against demand variance and lead-time volatility:"
    )

    add_equation_block(
        doc,
        "\\text{Safety Stock (SS)} = Z_{\\alpha} \\cdot \\sqrt{\\overline{LT} \\cdot \\sigma_D^2 + \\overline{D}^2 \\cdot \\sigma_{LT}^2}, \\qquad \\text{ROP} = (\\overline{D} \\cdot \\overline{LT}) + \\text{SS}",
        eq_num="Eq. 8.3",
        explanation="Statistical safety stock and reorder point formulations where Z_alpha = 1.645 (95% service level), LT is lead time, and D is daily demand."
    )

    doc.add_page_break()


def build_chapter_9(doc):
    """Builds Chapter 9: Demand Forecasting Engine."""
    add_heading_1(doc, "9. Demand Forecasting Engine")

    add_heading_2(doc, "9.1 Mathematical Problem Formulation")
    add_paragraph(
        doc,
        "Accurate demand forecasting is the vital first line of defense against the Bullwhip Effect in multi-echelon supply chains. "
        "Formally, given a historical univariate sales time-series $Y = \\{y_1, y_2, \\dots, y_t\\}$, the objective is to predict future demand "
        "$\\hat{y}_{t+h}$ over a multi-horizon forecast window $h \\in [1, 8]$ weeks ahead."
    )

    add_heading_2(doc, "9.2 Chronological Partitioning & Feature Extraction")
    add_paragraph(
        doc,
        "To guarantee academic validity and prevent future data leakage, data partitioning must strictly respect the arrow of time. "
        "Random cross-validation (which trains on future dates to predict past dates) was strictly forbidden. The 421,570 records of the Walmart "
        "dataset were split chronologically: Training: First 70%, Validation: Next 15%, Test: Final 15%."
    )
    add_paragraph(
        doc,
        "A feature matrix $X_t \\in \\mathbb{R}^{14}$ was engineered for every time step $t$ (`pipeline/feature_engineering.py`):"
    )

    fe_headers = ["Feature Category", "Variable Name", "Mathematical Definition", "Operational Rationale"]
    fe_data = [
        ["Calendar Seasonality", "month, week, quarter", "dt.month, dt.isocalendar().week", "Captures annual holiday cycles and monthly purchasing patterns"],
        ["Calendar Seasonality", "day_of_year", "dt.dayofyear", "Captures fine-grained seasonal progression"],
        ["Deterministic Trend", "trend", "t = 0, 1, 2, ..., N", "Captures baseline organic consumption growth across time"],
        ["Autoregressive Lags", "lag_1", "y_{t-1} = y.shift(1)", "Immediate prior week demand velocity (strongest single predictor)"],
        ["Autoregressive Lags", "lag_2, lag_4, lag_8", "y_{t-k} = y.shift(k)", "Captures bi-weekly, monthly, and bi-monthly consumption momentum"],
        ["Rolling Statistics", "rolling_mean_4", "\\frac{1}{4} \\sum_{i=1}^4 y_{t-i}", "Smooths short-term noise to establish 1-month moving baseline"],
        ["Rolling Statistics", "rolling_std_4", "\\sqrt{\\frac{1}{3} \\sum_{i=1}^4 (y_{t-i} - \\mu_4)^2}", "Measures short-term demand volatility and surge uncertainty"],
        ["Rolling Statistics", "rolling_mean_8", "\\frac{1}{8} \\sum_{i=1}^8 y_{t-i}", "Establishes medium-term 2-month quarterly demand trend"],
        ["Rolling Statistics", "rolling_max_4, min_4", "\\max_{i=1..4} y_{t-i}, \\min_{i=1..4} y_{t-i}", "Establishes dynamic upper and lower consumption boundaries"]
    ]

    add_custom_table(
        doc,
        headers=fe_headers,
        data=fe_data,
        col_widths=[Inches(1.4), Inches(1.4), Inches(1.8), Inches(1.9)],
        alignment=['L', 'L', 'L', 'L'],
        title="Table 9.1 — Autoregressive Lag & Rolling Window Feature Set (14 Variables)"
    )

    add_heading_2(doc, "9.3 Evaluated Baseline Models & XGBoost Regressor")
    add_paragraph(doc, "To prove genuine machine learning value-add, NEXUS benchmarks four alternative modeling techniques:")
    add_bullet(doc, "Naive Persistence Baseline: Assumes future demand equals the last observed value: $\\hat{y}_{t+h} = y_t$.", bold_prefix="1. Naive Model:")
    add_bullet(doc, "4-Week Moving Average: Averages the preceding 4 weeks: $\\hat{y}_{t+h} = \\frac{1}{4} \\sum_{i=0}^3 y_{t-i}$.", bold_prefix="2. Moving Average (4W):")
    add_bullet(doc, "8-Week Moving Average: Averages the preceding 8 weeks: $\\hat{y}_{t+h} = \\frac{1}{8} \\sum_{i=0}^7 y_{t-i}$.", bold_prefix="3. Moving Average (8W):")
    add_bullet(doc, "XGBoost Regressor (NEXUS): Gradient boosted regression trees optimizing squared error loss with tree depth 4, 150 estimators, learning rate $\\eta = 0.05$, and recursive multi-step autoregressive rollout.", bold_prefix="4. XGBoost Regressor:")

    add_heading_2(doc, "9.4 Empirical Evaluation & Benchmark Results")
    add_paragraph(
        doc,
        "Models were evaluated on the strictly held-out chronological test set using three standard metrics: "
        "Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Symmetric Mean Absolute Percentage Error (sMAPE):"
    )

    fc_headers = ["Forecasting Model Architecture", "MAE (Units)", "RMSE (Units)", "sMAPE (%)", "Error Reduction vs Naive", "Benchmark Rank"]
    fc_data = [
        ["XGBoost Regressor (NEXUS)", "68,553.14", "96,042.50", "4.35%", "-29.51% (Winner)", "1st Place"],
        ["Naive Persistence Baseline", "110,961.63", "136,255.10", "7.20%", "Baseline (0.0%)", "2nd Place"],
        ["4-Week Moving Average", "135,495.41", "153,446.84", "8.42%", "+12.62% higher error", "3rd Place"],
        ["8-Week Moving Average", "194,063.88", "210,775.27", "11.80%", "+54.69% higher error", "4th Place"]
    ]

    add_custom_table(
        doc,
        headers=fc_headers,
        data=fc_data,
        col_widths=[Inches(1.8), Inches(1.0), Inches(1.0), Inches(0.9), Inches(1.1), Inches(0.7)],
        alignment=['L', 'R', 'R', 'R', 'C', 'C'],
        title="Table 9.2 — Demand Forecasting Model Benchmark Comparison on Test Set"
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/14_model_benchmarks_chart.png",
        "Figure 9.1 — Demand Forecasting Error Comparison (Left) & Supplier Risk Out-of-Sample Metrics (Right)",
        width=Inches(5.4)
    )

    add_callout(
        doc,
        "EMPIRICAL ML BENCHMARK FINDING:\n"
        "The lag-engineered XGBoost Regressor achieved an RMSE of 96,042.50 units on the strictly held-out test set, "
        "representing a 29.51% error reduction over the Naive persistence baseline and a 37.41% error reduction over the 4-week "
        "Moving Average. This confirms that nonlinear gradient boosted trees effectively capture complex retail demand seasonality "
        "and holiday surges that linear moving averages fail to track.",
        alert_type="TIP",
        title="VERIFIED FORECASTING PERFORMANCE"
    )

    doc.add_page_break()


def build_chapter_10(doc):
    """Builds Chapter 10: Supervised Supplier Risk Prediction Engine."""
    add_heading_1(doc, "10. Supervised Supplier Risk Prediction Engine")

    add_heading_2(doc, "10.1 Business Rationale & Feature Space")
    add_paragraph(
        doc,
        "Modern multi-echelon networks cannot afford to wait for suppliers to officially declare force majeure or breach delivery SLAs. "
        "NEXUS implements a supervised predictive classification engine (`ml/risk/supplier_risk_model.py`) that continuously monitors eight "
        "operational strain features to predict the probability of imminent vendor disruption $P(y=1|x)$."
    )

    risk_feat_headers = ["Feature Name", "Data Type", "Measurement Unit", "Description & Operational Stress Interpretation"]
    risk_feat_data = [
        ["on_time_rate", "Float [0, 1]", "Percentage", "Empirical historical fulfillment ratio. Declines indicate early factory production bottlenecks."],
        ["average_delay", "Float", "Days", "Mean shipment delay duration when orders are late. Measures delay severity."],
        ["delay_frequency", "Float [0, 1]", "Probability", "Fraction of dispatched purchase orders that experienced shipping delays."],
        ["quality_score", "Float [0, 1]", "QA Ratio", "Incoming material acceptance ratio. Spikes in rejected parts indicate factory quality control breakdown."],
        ["lead_time", "Float", "Days", "Nominal delivery lead-time duration from order placement to warehouse dock arrival."],
        ["lead_time_variability", "Float", "Std Dev (Days)", "Standard deviation of delivery lead-time. High volatility indicates chaotic internal supplier logistics."],
        ["capacity_utilization", "Float [0, 1]", "Ratio", "Plant throughput load ratio. Vendors operating at >90% utilization cannot absorb minor equipment downtime."],
        ["historical_delays", "Integer", "Count", "Cumulative count of recorded past late shipments over the preceding 12 months."]
    ]

    add_custom_table(
        doc,
        headers=risk_feat_headers,
        data=risk_feat_data,
        col_widths=[Inches(1.5), Inches(1.0), Inches(1.1), Inches(2.9)],
        alignment=['L', 'C', 'C', 'L'],
        title="Table 10.1 — Supervised Supplier Risk Features & Definitions"
    )

    add_heading_2(doc, "10.2 Resolution of Data Leakage & Group Partitioning")
    add_paragraph(
        doc,
        "During the Phase 2 Credibility Audit, an exhaustive code review identified that initial prototypes suffered from "
        "**circular synthetic labeling** and **intra-vendor data leakage**. The target was originally generated via a deterministic rule "
        "(`target = 1 if otr < 0.92`), and random splitting placed observations from the same supplier across both train and test sets, "
        "producing artificial 1.0000 perfection.",
        bold_prefix="The Credibility Audit Fix:"
    )
    add_paragraph(
        doc,
        "The methodology was completely rebuilt to achieve genuine industrial-grade evaluation:\n"
        "1. Independent Latent Failure DGP: Target disruption status is generated from a multi-factor latent stress process combining delay frequency, "
        "quality defects, lead time volatility, capacity strain, and an independent stochastic shock (epsilon ~ N(0, 0.35)).\n"
        "2. Strict Group-Based Out-of-Sample Partitioning: Evaluated via `GroupShuffleSplit(n_splits=1, test_size=0.25)` across 40 distinct vendor operational "
        "profiles (480 monthly records). The 10 test vendors were completely unseen during training, guaranteeing zero vendor leakage."
    )

    add_heading_2(doc, "10.3 Logistic Regression vs. XGBoost Classifier")
    add_paragraph(
        doc,
        "NEXUS benchmarks a balanced Logistic Regression baseline against an advanced XGBoost Classifier (`scale_pos_weight = 1.5`, depth 3, `lr = 0.08`):"
    )

    risk_eval_headers = ["Supervised Model Architecture", "Precision", "Recall", "F1-Score", "ROC-AUC", "Evaluation Mode"]
    risk_eval_data = [
        ["Logistic Regression Baseline", "0.7531", "0.7349", "0.7439", "0.7401", "Out-of-Sample (Unseen Vendors)"],
        ["XGBoost Classifier (NEXUS)", "0.7442", "0.7711", "0.7574", "0.6988", "Out-of-Sample (Unseen Vendors)"]
    ]

    add_custom_table(
        doc,
        headers=risk_eval_headers,
        data=risk_eval_data,
        col_widths=[Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.1)],
        alignment=['L', 'R', 'R', 'R', 'R', 'C'],
        title="Table 10.2 — Supervised Supplier Risk Out-of-Sample Performance Benchmarks"
    )

    add_heading_2(doc, "10.4 Feature Importance & Model Explainability")
    add_paragraph(
        doc,
        "A critical strength of the NEXUS risk engine is **transparency**. Rather than acting as an inscrutable black box, the XGBoost model "
        "calculates Gini-impurity feature importances that explain *why* a vendor was flagged as high-risk:"
    )
    add_bullet(doc, "lead_time_variability: 22.38% (Primary leading indicator of imminent supply chain collapse)", bold_prefix="1.")
    add_bullet(doc, "lead_time: 19.79% (Nominal lead time duration)", bold_prefix="2.")
    add_bullet(doc, "historical_delays: 12.71% (Cumulative chronic delay count)", bold_prefix="3.")
    add_bullet(doc, "average_delay: 12.13% (Mean delay duration)", bold_prefix="4.")
    add_bullet(doc, "on_time_rate: 12.02% (Historical SLA delivery ratio)", bold_prefix="5.")
    add_bullet(doc, "quality_score: 11.25% (Material acceptance ratio)", bold_prefix="6.")
    add_bullet(doc, "capacity_utilization: 6.11% (Factory load ratio)", bold_prefix="7.")
    add_bullet(doc, "delay_frequency: 3.62% (Late shipment frequency)", bold_prefix="8.")

    doc.add_page_break()


def build_chapter_11(doc):
    """Builds Chapter 11: Operational Anomaly Detection Engine."""
    add_heading_1(doc, "11. Operational Anomaly Detection Engine")

    add_heading_2(doc, "11.1 Algorithm: Isolation Forest Formulation")
    add_paragraph(
        doc,
        "While supervised models predict known failure modes, real-world supply chains frequently encounter unprecedented, black-swan anomalies. "
        "NEXUS implements an unsupervised anomaly detection engine (`ml/anomaly/isolation_forest_detector.py`) utilizing **Isolation Forests** "
        "(100 estimators, contamination rate alpha = 0.03, StandardScaler preprocessing)."
    )
    add_paragraph(
        doc,
        "Isolation Forest operates on the mathematical principle that anomalous data points require significantly fewer random partition splits "
        "to isolate than nominal points. Formally, for an operational event vector x across n transactions, the anomaly score s(x, n) is defined as:"
    )

    add_equation_block(
        doc,
        "s(x, n) = 2^{-\\frac{E(h(x))}{c(n)}}, \\qquad \\text{where } c(n) = 2\\ln(n - 1) + 0.5772156649 - \\frac{2(n - 1)}{n}",
        eq_num="Eq. 11.1",
        explanation="Isolation Forest anomaly score where E(h(x)) is the average path length across 100 isolation trees and c(n) is the average path length of unsuccessful searches in a Binary Search Tree."
    )

    add_heading_2(doc, "11.2 Monitored Signals & Anomaly Taxonomy")
    add_paragraph(
        doc,
        "The anomaly detector scans three operational signals: purchase order quantity, binary delivery late status, and lead-time deviation "
        "(actual shipping days minus scheduled days). When an anomaly score breaches the decision threshold (score < 0.0), NEXUS categorizes the event "
        "into a structured operational taxonomy:\n"
        "• UNUSUAL_DEMAND_SPIKE: Severe surge in ordered units (>3.5 sigma) signaling panic buying or sudden market shifts.\n"
        "• TRANSIT_DELAY_OUTLIER: Delivery transit delay exceeding standard distributions by >3 sigma, indicating port strikes or severe road washouts.\n"
        "• ORDER_PATTERN_ANOMALY: Erratic transaction order volume patterns requiring immediate supply chain buffer review."
    )

    doc.add_page_break()


def build_chapter_12(doc):
    """Builds Chapter 12: Cascading Impact Propagation Analysis."""
    add_heading_1(doc, "12. Cascading Impact Propagation Analysis")

    add_heading_2(doc, "12.1 NetworkX Directed Graph Modeling")
    add_paragraph(
        doc,
        "A localized disruption at a single factory can easily trigger catastrophic network-wide stockouts if dependencies are unmapped. "
        "NEXUS implements a graph-theoretic failure traversal engine (`impact/impact_engine.py`) built on a **NetworkX Directed Graph (DiGraph)**. "
        "The graph explicitly models multi-echelon precedence constraints:"
    )

    add_equation_block(
        doc,
        "\\mathcal{G} = (\\mathcal{V}, \\mathcal{E}), \\qquad \\mathcal{V} = \\mathcal{S} \\cup \\mathcal{P} \\cup \\mathcal{W} \\cup \\mathcal{H} \\cup \\mathcal{D}",
        eq_num="Eq. 12.1",
        explanation="Directed network graph where V represents 83 facility nodes (Suppliers, Plants, Warehouses, Hubs, Demand Zones) and E represents 160 transit corridors."
    )

    add_heading_2(doc, "12.2 Multi-Echelon Failure Traversal Algorithm")
    add_paragraph(
        doc,
        "When an entity is disrupted (e.g., Supplier SUP_001 suffers an 80% capacity cut for 10 days), the ImpactEngine traverses downstream dependencies:\n"
        "1. Dependent SKU Discovery: Queries the catalog for all products where `primary_supplier_id == SUP_001` (identifying PROD_ITEM_003).\n"
        "2. Corridor & Warehouse Mapping: Traces outbound routes to identify downstream warehouses (WH_01 Western Depot, WH_08 Northern Depot).\n"
        "3. Inventory Runway Calculation: Computes the exact operational runway days remaining at each warehouse:\n"
        "   $$\\text{Runway (Days)} = \\frac{\\text{Current Warehouse Stock}}{\\text{Average Daily Consumption Rate}}$$\n"
        "   If Runway < Disruption Duration (10 Days), a stockout breach is flagged (e.g., WH_01 runway = 4.7 days -> stockout imminent on Day 5).\n"
        "4. Demand Zone Exposure: Traverses outbound routes from compromised warehouses to identify exposed consumer markets (5 demand zones).\n"
        "5. Shortage & Service Level Estimation: Quantifies potential unmet demand and projects service level collapse:\n"
        "   $$\\text{Lost Capacity} = \\text{Capacity} \\times 0.80 \\times \\left(\\frac{10}{30}\\right) = 3,200\\text{ units}, \\qquad \\text{Projected SL} = 63.0\\%\\text{ (-35.0\\% drop)}$$\n"
        "6. Alternative Supplier Discovery: Automatically scans the digital twin to discover qualified alternative suppliers with spare capacity (Sanand Precision Casting SUP_004, Hero Fasteners SUP_015)."
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/05_impact_analysis.png",
        "Figure 12.1 — Disruption Impact Propagation Engine (Screen 5: Cascade Pipeline, Stock Runways, and Alternative Vendors)",
        width=Inches(5.0)
    )

    doc.add_page_break()


def build_chapter_13(doc):
    """Builds Chapter 13: Scenario Simulation Studio."""
    add_heading_1(doc, "13. Scenario Simulation Studio")

    add_heading_2(doc, "13.1 In-Memory Copy-on-Write State Cloning")
    add_paragraph(
        doc,
        "A foundational design principle of NEXUS is **non-destructive scenario simulation**. Planners must be empowered to test extreme "
        "'what-if' shock hypotheses without risking database corruption. The Scenario Simulation Engine (`simulation/scenario_engine.py`) enforces "
        "strict in-memory state isolation using a copy-on-write `SimulationState` object."
    )
    add_paragraph(
        doc,
        "When a simulation request arrives, the engine deep-copies all suppliers, warehouses, routes, and demand zones from the database session "
        "into memory. Disruption shocks mutate *only* the ephemeral clone. Once the simulation and optimization calculations complete, the clone is "
        "discarded, leaving the persistent database 100% unaltered."
    )

    add_heading_2(doc, "13.2 Five Verified Disruption Shock Scenarios")
    add_paragraph(doc, "NEXUS provides native support for five distinct operational disruption scenarios:")

    scen_headers = ["Scenario Identifier", "Target Parameters", "Simulation Mechanism & Transformation", "Downstream Propagation Effect"]
    scen_data = [
        ["SUPPLIER_FAILURE", "supplier_id, capacity_reduction (0-1), duration_days", "Scales supplier capacity down (e.g. -80%), marks status as DISRUPTED, elevates risk score to 0.85", "Triggers component shortage, drains warehouse stock runway, exposes dependent consumer zones"],
        ["ROUTE_DISRUPTION", "route_id, duration_days", "Sets corridor status to BLOCKED, sets throughput capacity to 0.0", "Forces freight detours, recalculates highway transit times, inflates transportation costs"],
        ["DEMAND_SPIKE", "demand_spike_percent (0-1), optional zone_id", "Multiplies consumer demand volume by (1 + spike_pct) across target or network-wide zones", "Tests safety stock adequacy, stresses supplier throughput limits, risks stockout penalties"],
        ["WAREHOUSE_SHUTDOWN", "warehouse_id, duration_days", "Sets warehouse status to SHUTDOWN, sets capacity to 0.0, automatically severs all inbound & outbound routes", "Immobilizes inventory, severs distribution corridors, causes localized consumer stockouts"],
        ["COMBINED_DISRUPTION", "supplier_id, route_id, demand_spike, duration", "Concurrently executes supplier capacity cuts, transit corridor severances, and regional demand surges", "Simulates compound systemic disasters (e.g., severe monsoon flooding + regional labor strike)"]
    ]

    add_custom_table(
        doc,
        headers=scen_headers,
        data=scen_data,
        col_widths=[Inches(1.4), Inches(1.3), Inches(2.0), Inches(1.8)],
        alignment=['L', 'L', 'L', 'L'],
        title="Table 13.1 — Supported Operational Disruption Scenarios & Shock Parameters"
    )

    add_image_with_caption(
        doc,
        "NEXUS_Documentation_Assets/06_scenario_simulation.png",
        "Figure 13.1 — What-If Scenario Simulation Studio (Screen 6: Five Disruption Tabs and Before vs. After State Comparison)",
        width=Inches(5.0)
    )

    doc.add_page_break()
