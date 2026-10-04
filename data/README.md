# NEXUS Data Foundation & Digital Twin Provenance

This directory contains the multi-echelon data foundation powering the **NEXUS** decision-intelligence engine. To maintain academic and scientific integrity, all data sources, transformations, and simulation models are explicitly categorized below.

---

## 1. Data Classification Matrix

| Dataset / Entity | Source Type | Original Provider | Description & Provenance |
| :--- | :--- | :--- | :--- |
| **Walmart Weekly Sales** (`train.csv`) | **Public / Empirical** | Kaggle / Walmart Recruiting | Real-world historical retail sales across 45 stores and 99 departments (2010–2012) with markdown events and CPI. |
| **DataCo Global Supply Chain** (`dataco_supply_chain.csv`) | **Public / Empirical** | Kaggle / DataCo Global | Real-world transactional records capturing order fulfillment, shipment modes, delivery delays, and customer locations. |
| **Processed Demand Series** (`walmart_demand_cleaned.parquet`) | **Transformed** | NEXUS Pipeline | Aggregated, cleaned, and feature-engineered time-series with 7/14/30-day rolling statistics and calendar features. |
| **Processed Logistics Logistics** (`dataco_logistics_cleaned.parquet`) | **Transformed** | NEXUS Pipeline | Cleaned shipment logs normalized for transit lead time variance and late-delivery risk modeling. |
| **Indian Digital Twin Network** (`data/processed/*.csv`) | **Calibrated Simulation** | Generated / Calibrated | 83 synthetic facility nodes across India (40 suppliers, 8 manufacturing units, 15 hubs, 20 retail demand zones). |
| **Transit Corridors** (`routes.csv`) | **Geospatial / Calibrated** | OpenStreetMap / Haversine | 160 multimodal transit routes with real geographic coordinates, toll costs, and road/rail transit lead times. |
| **Relational Database** (`nexus.db`) | **Local Artifact** | SQLite Engine | Operational relational schema populated deterministically from empirical and calibrated sources. |

---

## 2. Dataset Overviews

### A. Empirical Retail Demand: Walmart Weekly Sales
* **Path**: `data/raw/train.csv` (12.8 MB)
* **Description**: Historical weekly sales series capturing holiday surges (Super Bowl, Labor Day, Thanksgiving, Christmas), local economic indicators, and demand variance.
* **Usage in NEXUS**: Used to train and benchmark multi-horizon forecasting models (XGBoost, Facebook Prophet, Holt-Winters Exponential Smoothing) in `ml/forecasting/`.
* **Preprocessing**: Null values imputed, date indices regularized, and lag features ($t-1, t-2, t-4, t-12$) generated strictly backward-looking to eliminate future lookahead bias.

### B. Empirical Logistics & Fulfillment: DataCo Global Supply Chain
* **Path**: `data/raw/dataco_supply_chain.csv` (14.2 MB)
* **Description**: Multi-year order records detailing delivery status, scheduled vs. real transit days, late delivery risks, and order processing workflows.
* **Usage in NEXUS**: Supplies real operational delay variance, defect frequencies, and late-shipment distributions used to parameterize the multi-factor supplier risk models.

### C. Indian Logistics Digital Twin
* **Path**: `data/processed/` (suppliers.csv, warehouses.csv, demand_zones.csv, routes.csv, products.csv)
* **Description**: Spatial and operational network topology modeling India's manufacturing and distribution landscape across major industrial corridors (Delhi-NCR, Mumbai-Pune, Chennai-Bengaluru, Gujarat, Kolkata).
* **Usage in NEXUS**: Forms the graph network topology (`digital_twin/network_graph.py`) and linear programming constraints (`optimization/ortools_optimizer.py`).
* **Disclaimer**: Facility names and operational capacities represent a **calibrated synthetic digital twin** for decision-intelligence simulation. They do not represent live proprietary telemetry from private industrial operators.

---

## 3. Directory Layout

```
data/
├── README.md                           # This provenance document
├── raw/                                # Pristine empirical datasets
│   ├── dataco_supply_chain.csv         # DataCo supply chain transactions
│   └── train.csv                       # Walmart weekly sales series
├── processed/                          # Pipeline-transformed features & network topology
│   ├── dataco_logistics_cleaned.parquet# Cleaned delivery lead times
│   ├── demand_zones.csv                # 20 consumption centroids
│   ├── products.csv                    # Product catalog & bill-of-materials
│   ├── routes.csv                      # 160 transit corridors with distances & freight rates
│   ├── suppliers.csv                   # 40 multi-tier supplier profiles
│   ├── walmart_demand_cleaned.parquet  # Feature-engineered demand time-series
│   └── warehouses.csv                  # 23 distribution hubs & fulfillment centers
└── nexus.db                            # SQLite relational database (generated via pipeline)
```

---

## 4. Reproducibility & Pipeline Execution

The complete database can be reproduced deterministically from the raw data files with:

```bash
# Generate processed tables and populate SQLite database
python run_pipeline.py
```

* **Determinism**: Random seeds (`RANDOM_SEED=42`) are fixed in `backend/app/config.py` across network generation, train/test splitting, and synthetic disruption injection.
* **Database Portability**: The database engine automatically falls back to SQLite (`data/nexus.db`) for lightweight local execution, while fully supporting PostgreSQL in containerized and cloud production environments via `DATABASE_URL`.
