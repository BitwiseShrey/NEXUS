# NEXUS Machine Learning Architecture & Model Evaluation

## 1. Executive Summary

Machine learning in NEXUS serves three critical functions:
1. **Demand Forecasting**: Estimating future demand velocity to prevent stockouts and Bullwhip distortion.
2. **Supplier Disruption Risk Prediction**: Predicting probability of vendor failure before catastrophic stockouts occur.
3. **Operational Anomaly Detection**: Identifying sudden demand surges, lead-time delays, and anomalous order patterns in real time.

All models adhere to academic standards: baseline comparison benchmarks, chronological time-series splitting (no future data leakage), and imbalanced classification metrics.

---

## 2. Demand Forecasting Engine

### 2.1 Problem Formulation & Splitting Strategy
Given an empirical demand time-series $y_1, y_2, \dots, y_t$, the objective is to predict future demand $\hat{y}_{t+h}$ over a multi-step horizon $h \in [1, 12]$ weeks.

To prevent temporal data leakage, data is partitioned chronologically:
- **Training Set**: First 70% of chronological observations.
- **Validation Set**: Next 15% (used for early stopping and hyperparameter calibration).
- **Test Set**: Final 15% (strictly held-out for unbiased benchmark evaluation).

### 2.2 Feature Engineering
The feature matrix $X_t$ incorporates 14 autoregressive and calendar variables:
- **Autoregressive Lags**: $y_{t-1}, y_{t-2}, y_{t-4}, y_{t-8}$
- **Rolling Window Statistics**: 4-week mean $\mu_4$, 4-week standard deviation $\sigma_4$, 8-week mean $\mu_8$, 4-week max, 4-week min
- **Calendar Seasonality**: Month, ISO week of year, quarter, day of year
- **Deterministic Trend**: Time index $t$

All rolling statistics are lagged by 1 period ($\text{shift}(1)$) to ensure no lookahead bias occurs.

### 2.3 Models Evaluated

1. **Naive Persistence Baseline**:
   $$\hat{y}_{t+h} = y_t$$
2. **4-Week Moving Average Baseline**:
   $$\hat{y}_{t+h} = \frac{1}{4}\sum_{i=0}^3 y_{t-i}$$
3. **8-Week Moving Average Baseline**:
   $$\hat{y}_{t+h} = \frac{1}{8}\sum_{i=0}^7 y_{t-i}$$
4. **XGBoost Regressor**:
   Gradient boosted regression trees optimizing squared error loss with tree depth 4, 150 estimators, learning rate $\eta = 0.05$, and feature sub-sampling:
   $$\mathcal{L}^{(t)} = \sum_{i=1}^n l\left(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)\right) + \Omega(f_t)$$

### 2.4 Empirical Benchmark Results (Walmart Dataset)

| Model | MAE | RMSE | sMAPE (%) | Rank |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost Regressor (NEXUS)** | **68,553.14** | **96,042.50** | **4.35%** | **1 (Winner)** |
| Naive Persistence | 110,961.63 | 136,255.10 | 7.20% | 2 |
| Moving Average (4-Week) | 135,495.41 | 153,446.84 | 8.42% | 3 |
| Moving Average (8-Week) | 194,063.88 | 210,775.27 | 11.80% | 4 |

**Key Finding**: The XGBoost Regressor reduced RMSE by **29.5%** over the Naive baseline and **37.4%** over the 4-week Moving Average.

---

## 3. Supplier Risk Prediction Model

### 3.1 Problem Formulation & Target
Supply chain disruptions are rare but high-consequence events. A binary classification target $y \in \{0, 1\}$ was formulated:
- $y = 1$: High risk / disruption event (supplier SLA breach, critical delay, or failure).
- $y = 0$: Nominal operational status.

### 3.2 Predictive Features
1. `on_time_rate`: Empirical historical fulfillment ratio
2. `average_delay`: Mean delay days when shipments are late
3. `delay_frequency`: Probability of late dispatch
4. `quality_score`: Material acceptance QA ratio
5. `lead_time`: Nominal lead-time days
6. `lead_time_variability`: Standard deviation of delivery lead-time
7. `capacity_utilization`: Plant load ratio
8. `historical_delays`: Cumulative historical delay count

### 3.3 Models Evaluated

1. **Baseline Model**: Logistic Regression with balanced class weights:
   $$P(y=1|x) = \sigma(w^T x + b)$$
2. **Advanced Model**: XGBoost Classifier with `scale_pos_weight = 1.5`, max depth 3, learning rate 0.08:
   Optimized with log-loss on stratified train/test partitions.

### 3.4 Evaluation Metrics (Audited Out-of-Sample Evaluation)

Prior iterations suffered from synthetic circular labeling (a deterministic threshold on `on_time_rate < 0.92`), which caused artificial 1.0000 perfection on random splits.

Following the Phase 2 Credibility Audit, the methodology was completely re-engineered:
1. **Independent Latent Failure DGP**: Disruption probability is generated from multi-factor latent strain (delay frequency, quality defects, lead time volatility, capacity strain, and historical delay volume) combined with realistic stochastic logistic shock ($\epsilon \sim \mathcal{N}(0, 0.35)$).
2. **Strict Group-Based Out-of-Sample Partitioning**: Evaluated via `GroupShuffleSplit(test_size=0.25)` across 40 distinct vendor operational profiles (480 monthly records). The 10 test vendors are completely unseen during training.

| Model | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression Baseline | 0.7531 | 0.7349 | 0.7439 | 0.7401 |
| **XGBoost Classifier (NEXUS)** | **0.7442** | **0.7711** | **0.7574** | **0.6988** |

### 3.5 Model Explainability & Feature Importance
The trained XGBoost model surfaces empirical operational risk drivers across unseen vendors:
- `lead_time_variability`: **22.38%** (Primary leading indicator of supply collapse)
- `lead_time`: **19.79%**
- `historical_delays`: **12.71%**
- `average_delay`: **12.13%**
- `on_time_rate`: **12.02%**
- `quality_score`: **11.25%**
- `capacity_utilization`: **6.11%**
- `delay_frequency`: **3.62%**

Feature importance is directly exposed in the API (`POST /api/v1/risk/predict`) to explain *why* a supplier is flagged as critical.

---

## 4. Anomaly Detection Engine

### 4.1 Algorithm: Isolation Forest
Unsupervised multi-variate anomaly detection is implemented using `IsolationForest` ($N_{\text{estimators}} = 100$, contamination rate $\alpha = 0.03$).

Isolation Forest isolates anomalies by randomly partitioning feature dimensions:
$$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
Anomalies require significantly fewer random splits to isolate than normal instances.

### 4.2 Signals Monitored
- Unusual demand spikes (order quantities exceeding standard distribution bounds)
- Unprecedented transit delays (lead-time deviation $> 3\sigma$)
- Irregular order velocity

### 4.3 Output Taxonomy
- `UNUSUAL_DEMAND_SPIKE`: Severe surges requiring production and warehouse buffer rebalancing.
- `TRANSIT_DELAY_OUTLIER`: Unexpected logistics bottlenecks.
- `ORDER_PATTERN_ANOMALY`: Erratic ordering patterns.
- Normalized severity score $[0.0, 1.0]$.
