# NEXUS — End-to-End Demonstrative Disruption Scenario

## Scenario Overview
This document records an end-to-end, reproducible execution of the complete NEXUS decision-intelligence loop:
$$\mathbf{MONITOR} \longrightarrow \mathbf{PREDICT} \longrightarrow \mathbf{ANALYZE\ IMPACT} \longrightarrow \mathbf{SIMULATE} \longrightarrow \mathbf{OPTIMIZE} \longrightarrow \mathbf{RECOMMEND}$$

- **Seed**: `42`
- **Solver**: Google OR-Tools (Linear Solver GLOP)
- **Disrupted Node**: `SUP_001` (Tata AutoComp Components, Pune Chakan Hub)
- **Disruption Parameter**: 80% Capacity Loss for 10 Days
- **Objective**: Minimize Total Supply Chain Operational Cost (Procurement + Freight + Holding + Shortage Penalties + Risk Penalties)

---

## 1. Initial State (Normal Operations)
Prior to failure injection, the calibrated digital twin network exhibits the following baseline telemetry:

- **Total Active Suppliers**: 20
- **Total SKUs Tracked**: 500 across 10 central warehouses
- **Total Network Inventory Valuation**: INR 45,916,967.54
- **Historical Orders Evaluated**: 10,000 (calibrated from DataCo logistics records)
- **Baseline On-Time Delivery SLA**: 83.03%
- **Network Gross Capacity Balance**: +205,000 units (supply exceeds average demand under normal conditions)

---

## 2. Disruption Injection
- **Target Node**: Supplier `SUP_001`
- **Location**: Pune (Chakan), Maharashtra
- **Product Category**: Automotive Precision Components
- **Normal Throughput Capacity**: 12,000 units/period
- **Injected Shock**: 80% Capacity Reduction ($12,000 \to 2,400$ units/period)
- **Duration**: 10 days
- **Simulated Trigger**: Unscheduled boiler failure / regional labor strike

---

## 3. Disruption Impact Propagation
The NetworkX directed graph engine traverses downstream dependencies:

- **Directly Dependent Product**: `PROD_ITEM_003` (Tier-1 automotive subassembly)
- **Direct Downstream Warehouses**: 2 (`WH_01` Western Central Warehouse, `WH_02` Northern Logistics Center)
- **Affected Demand Zones**: 5 (`ZONE_01` Mumbai Metro, `ZONE_02` Pune Industrial, `ZONE_03` Delhi NCR, `ZONE_04` Jaipur, `ZONE_05` Ahmedabad)
- **Warehouse Runway Analysis**:
  - `WH_01`: Current Stock = 1,420 units | Daily Burn Rate = 280 units/day | Runway = 5.07 days $\to$ **Stockout Expected on Day 6**
  - `WH_02`: Current Stock = 3,100 units | Daily Burn Rate = 310 units/day | Runway = 10.0 days $\to$ Buffer adequate, borderline
- **Shortage Projected Without Reallocation**: 69,843.2 units

---

## 4. In-Memory Scenario Simulation
The `ScenarioEngine` forks a non-destructive state clone:

- **Total Network Demand**: 153,600.0 units
- **Total Available Supplier Capacity Post-Shock**: 314,350.2 units
- **Net System Capacity Balance**: +160,750.2 units
- **Key Insight**: The network as a whole retains sufficient physical capacity to absorb the shock, but rigid static allocations create severe localized stockouts.

---

## 5. Optimization vs. Baseline Comparison

| Operational Metric | Unoptimized Baseline (Heuristic) | NEXUS Optimized (Google OR-Tools GLOP) | Differential Impact / Value-Add |
| :--- | :---: | :---: | :---: |
| **Total Operational Cost** | INR 41,215,184.70 | **INR 19,291,240.54** | **-53.19% (Cost Saved: INR 21,923,944.16)** |
| **Procurement Cost** | INR 12,410,250.00 | INR 15,820,140.54 | +INR 3,409,890.54 (Higher volume procured) |
| **Freight / Transportation** | INR 1,845,220.00 | INR 3,471,100.00 | +INR 1,625,880.00 (Agile cross-hub rerouting) |
| **Shortage Penalty Cost** | INR 24,445,120.00 | **INR 0.00** | **-100% (INR 24.4M penalties eliminated)** |
| **Holding Cost** | INR 2,514,594.70 | INR 0.00 | In-transit agile cross-docking |
| **Unmet Demand (Shortages)** | 69,843.2 units | **0.0 units** | **69,843.2 units fulfilled** |
| **Network Service Level** | 54.57% | **100.00%** | **+45.43 percentage points** |
| **Solver Execution Time** | N/A (Rule-based) | **0.0061 seconds** | Real-time enterprise decision support |

---

## 6. How the 53.19% Savings is Achieved
1. **Unoptimized Heuristic Baseline**:
   - Rigid single-sourcing causes demand zones to fail when primary suppliers drop capacity.
   - Severe shortages ($69,843.2$ units) incur massive contractual SLA penalties ($\text{INR } 350/\text{unit} = \text{INR } 24,445,120$).
2. **NEXUS Optimization**:
   - The linear program solves global multi-echelon assignment across all 20 suppliers and 10 warehouses simultaneously.
   - Procurement shifts slightly to secondary qualified suppliers (`SUP_005` Tata Steel, `SUP_009` Kumaon Polymer, `SUP_010` Surat Synthetic).
   - Higher freight and procurement expenditures (+INR 5.03M) completely eliminate INR 24.45M in stockout penalties.
   - **Net ROI**: $\text{INR } 24.45\text{M penalties avoided} - \text{INR } 5.03\text{M rerouting costs} = \mathbf{INR\ 21.92M\ net\ savings}$.

---

## 7. Synthesized Actionable Recommendation

- **Directives ID**: `REC_AUTO_MITIGATION_SUP001`
- **Title**: *Mitigation Strategy for Tata AutoComp Components Disruption (SUPPLIER_FAILURE [SUP_001])*
- **Executive Rationale**:
  > "Risk analysis detected that Tata AutoComp Components (SUP_001) faces significant capacity degradation over a projected 10-day window. Without intervention, baseline heuristic operations would cause a shortage of 69,843.2 units, dropping network service levels to 54.6%."
- **Recommended Actions**:
  1. *Shift 18.5% (25,000 units) of raw material procurement to `SUP_005` (Jamshedpur).*
  2. *Shift 12.0% (16,200 units) of component buffering to `SUP_009` (Pantnagar).*
  3. *Rebalance safety stock at `WH_01` by dispatching 1,800 units from `WH_04` via North-South Rail Freight Corridor.*
- **Expected Quantified Benefit**:
  > "Adopting the NEXUS optimized multi-echelon allocation reduces network shortage by 69,843.2 units, maintains service level at 100.0% (+45.43% vs baseline), and achieves net operational savings of INR 21,923,944.16 (53.19% cost reduction)."
- **Plan Robustness Score**: **0.98** (Derived from mathematical LP optimality: $\text{status} = \text{OPTIMAL}$, $\text{service level} = 100\%$, $\text{shortage mitigation} = 100\%$).
- **Simulated ERP/WMS Status**: Ready for demonstration dispatch to mock WMS/ERP queue.
