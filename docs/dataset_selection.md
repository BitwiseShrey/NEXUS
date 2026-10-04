# NEXUS Dataset Selection & Evaluation

## 1. Executive Summary & Data Strategy

NEXUS employs a **Hybrid Data Strategy**:
$$\text{Supply Chain Decision Intelligence} = \text{Real Empirical Patterns} + \text{Controlled Digital Twin} + \text{Spatial Topology}$$

Real-world enterprise supply chain data is typically proprietary and confidential. To achieve academic rigor, reproducibility, and industrial realism for this B.Tech capstone project, NEXUS incorporates two premier open-access empirical datasets for demand time-series and fulfillment risk patterns, mapped onto an Indian National Supply Chain Digital Twin network.

| Component | Nature of Data | Source / Foundation | Purpose in NEXUS |
| :--- | :--- | :--- | :--- |
| **Sales & Demand Series** | Real / Empirical | Walmart Store Sales Time-Series | Multi-horizon demand forecasting (baselines + XGBoost) |
| **Logistics & Delivery Risk** | Real / Empirical | DataCo Global Supply Chain Dataset | Lead times, delivery delays, transit variability, supplier risk modeling |
| **Facility Topology** | Controlled Synthetic | Indian Geospatial Hubs (Delhi, Mumbai, Bengaluru, etc.) | Warehouse, factory, and demand zone geographic nodes |
| **Disruption Scenarios** | Controlled Synthetic | Deterministic & Stochastic Scenario Injections | Stress testing, impact propagation, OR-Tools optimization |

---

## 2. Dataset 1: Walmart Store Sales Dataset

- **Dataset Name:** Walmart Recruiting - Store Sales Forecasting
- **Source:** Kaggle / Walmart Global Analytics (Public Research Dataset)
- **URL/Reference:** `https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting`
- **License / Usage Notes:** Public Academic & Research Use Allowed.
- **Number of Records:** 421,570 weekly historical records across 45 stores and 81 departments.
- **Historical Horizon:** February 2010 to October 2012 (~2.5+ years of continuous time-series data).

### Key Variables:
- `Store`: Facility identifier (mapped to Regional Demand Zones / Warehouses)
- `Dept`: Department category (mapped to Product Categories)
- `Date`: Timestamp of recorded sales
- `Weekly_Sales`: Volume of sales recorded (demand quantity metric)
- `IsHoliday`: Binary indicator of national holiday/demand surge

### Relevance to NEXUS:
Demand forecasting in supply chains requires genuine real-world properties: calendar seasonality, holiday surges, trends, and department-level cross-elasticity. Synthetically generated random sine-waves do not test real ML model generalization. The Walmart dataset provides genuine sales volatility to rigorously evaluate Moving Average, Naive baselines, and Lag-Engineered XGBoost Regressors.

### Preprocessing:
1. Filter top active categories and aggregate weekly timestamps into daily/weekly regular frequency.
2. Feature engineering: Calendar lags ($t-1, t-2, t-4, t-8$), rolling moving averages (4-week, 8-week), rolling volatility, month, day-of-year, and holiday flags.
3. Chronological train/validation/test split (no random leakage).

### Limitations:
- Records are aggregated weekly rather than hourly/daily transaction-level.
- Prices and inventory stock levels at the moment of sale are not provided in the sales table.

---

## 3. Dataset 2: DataCo Global Supply Chain Intelligence Dataset

- **Dataset Name:** DataCo Smart Supply Chain for Big Data Analysis
- **Source:** Mendeley Data / Kaggle / Constante et al. (Universidad de las Fuerzas Armadas)
- **URL/Reference:** `https://data.mendeley.com/datasets/8gx2fvg2k6/5` | `https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis`
- **License / Usage Notes:** Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Number of Records:** 35,000+ representative shipments processed from the full 180,519 order corpus.
- **Scope:** Multi-echelon logistics, delivery tracking, late delivery risk flags, freight modes.

### Key Variables:
- `Type`: Payment and order fulfillment type (DEBIT, TRANSFER, CASH, PAYMENT)
- `Days for shipping (real)`: Actual delivery transit time taken
- `Days for shipment (scheduled)`: SLA promise delivery transit time
- `Delivery Status`: Categorical delivery outcome (`Advance shipping`, `Late delivery`, `Shipping on time`, `Shipping canceled`)
- `Late_delivery_risk`: Binary ground-truth target (1 = Late, 0 = On Time)
- `Benefit per order`: Order profit/loss margin
- `Order Item Quantity`: Units ordered per line item
- `Sales`: Gross revenue per transaction
- `Shipping Mode`: Transport method (`Standard Class`, `First Class`, `Second Class`, `Same Day`)
- `Category Name`: Product department categorization

### Relevance to NEXUS:
NEXUS requires authentic delivery delays, lead-time variance, and fulfillment failure patterns to train the **Supplier Risk Prediction Model** and calibrate route transit times. By learning from actual historical lead-time deviations (where actual days > scheduled days), our risk engine learns realistic probability densities instead of arbitrary heuristics.

### Preprocessing:
1. Feature extraction: Lead-time deviation (`Days real - Days scheduled`), late delivery ratio per shipping mode, order size volatility.
2. Supplier performance aggregation: Calculation of historical on-time rates, quality scores, and capacity strain features.
3. Label encoding of shipping modes and fulfillment classes.

### Limitations:
- Specific real names of commercial suppliers are anonymized for privacy.
- Geographic origins are predominantly international; NEXUS maps these lead-time distributions to realistic Indian logistics hubs (Delhi-Mumbai-Bengaluru corridors).

---

## 4. Controlled Digital Supply Chain Twin Network

Because public datasets omit proprietary internal factory BOMs (Bills of Materials), multi-tier warehouse topologies, and exact geo-coordinates of Indian logistics corridors, NEXUS constructs a validated **Digital Supply Chain Twin**:

- **Suppliers ($N=20$):** Spanning Tier-1 and Tier-2 component and raw material vendors.
- **Production Units ($N=8$):** Manufacturing plants situated in industrial clusters (Sanand, Pune, Sriperumbudur, Gurgaon, etc.).
- **Products ($N=50$):** Spanning Criticality Levels 1 (Commodity) to 3 (Mission-Critical Component).
- **Warehouses ($N=10$):** Central and regional distribution centers.
- **Distribution Hubs ($N=15$):** Intermediate transit sorting nodes.
- **Demand Zones ($N=30$):** Tier-1 & Tier-2 Indian urban consumer zones.
- **Routes ($N=120+$):** Road, rail, and multimodal transit corridors with authentic Indian highway distances and transit durations.

All synthetic components strictly conform to the empirical distributions derived from the Walmart and DataCo datasets, ensuring realistic capacity ratios, safety stock levels, and cost structures.
