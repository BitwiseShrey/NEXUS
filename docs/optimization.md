# NEXUS Multi-Echelon Optimization Engine

## 1. Problem Formulation

The core mission of NEXUS is to translate predictive risk intelligence into optimal operational decisions. When a supply shock occurs, NEXUS formulates and solves a multi-echelon network flow optimization problem using **Google OR-Tools**.

```
[Suppliers S] ──(X_sw)──> [Warehouses W] ──(Y_wd)──> [Demand Zones D]
                                                            │
                                                        [Shortage U_d]
```

### 1.1 Sets and Indices
- $s \in \mathcal{S}$: Set of 20 suppliers
- $w \in \mathcal{W}$: Set of 10 fulfillment warehouses
- $d \in \mathcal{D}$: Set of 30 regional demand zones
- $\mathcal{B} \subset (\mathcal{S} \times \mathcal{W}) \cup (\mathcal{W} \times \mathcal{D})$: Set of currently severed/blocked corridors

### 1.2 Parameters
- $\text{Cap}_s$: Available production capacity of supplier $s$ (units)
- $\text{Cap}_w$: Storage/throughput capacity of warehouse $w$ (units)
- $\text{Demand}_d$: Projected demand at demand zone $d$ (units)
- $c_s^{\text{proc}}$: Procurement cost per unit from supplier $s$ (INR)
- $c_{s,w}^{\text{trans}}$: Freight transport cost from supplier $s$ to warehouse $w$ (INR)
- $c_{w,d}^{\text{trans}}$: Freight transport cost from warehouse $w$ to demand zone $d$ (INR)
- $c_w^{\text{hold}}$: Handling and holding cost per unit at warehouse $w$ (INR)
- $r_s$: Model-inferred risk score of supplier $s \in [0, 1]$
- $\lambda_{\text{risk}}$: Risk aversion penalty coefficient (default: 50.0)
- $p_{\text{shortage}}$: Shortage penalty cost per unmet unit (default: INR 350.0)

### 1.3 Decision Variables
- $X_{s, w} \ge 0$: Quantity procured from supplier $s$ and shipped to warehouse $w$.
- $Y_{w, d} \ge 0$: Quantity dispatched from warehouse $w$ to demand zone $d$.
- $U_d \ge 0$: Unmet shortage at demand zone $d$.

---

## 2. Mathematical Optimization Model

### 2.1 Objective Function
Minimize total operational cost, comprising procurement, freight, holding, shortage penalties, and risk exposure penalties:

$$\min \mathcal{Z} = \sum_{s \in \mathcal{S}} \sum_{w \in \mathcal{W}} \left(c_s^{\text{proc}} + c_{s,w}^{\text{trans}} + \lambda_{\text{risk}} \cdot r_s\right) X_{s, w} + \sum_{w \in \mathcal{W}} \sum_{d \in \mathcal{D}} \left(c_w^{\text{hold}} + c_{w,d}^{\text{trans}}\right) Y_{w, d} + \sum_{d \in \mathcal{D}} p_{\text{shortage}} \cdot U_d$$

### 2.2 Constraints

1. **Supplier Capacity**:
   $$\sum_{w \in \mathcal{W}} X_{s, w} \le \text{Cap}_s \quad \forall s \in \mathcal{S}$$

2. **Warehouse Inbound Throughput**:
   $$\sum_{s \in \mathcal{S}} X_{s, w} \le \text{Cap}_w \quad \forall w \in \mathcal{W}$$

3. **Warehouse Flow Conservation**:
   Outbound dispatches cannot exceed inbound receipts:
   $$\sum_{d \in \mathcal{D}} Y_{w, d} \le \sum_{s \in \mathcal{S}} X_{s, w} \quad \forall w \in \mathcal{W}$$

4. **Demand Satisfaction & Shortage Balance**:
   $$\sum_{w \in \mathcal{W}} Y_{w, d} + U_d = \text{Demand}_d \quad \forall d \in \mathcal{D}$$

5. **Corridor Feasibility (Disrupted Routes)**:
   $$X_{s, w} = 0 \quad \forall (s, w) \in \mathcal{B}$$
   $$Y_{w, d} = 0 \quad \forall (w, d) \in \mathcal{B}$$

6. **Non-negativity Bounds**:
   $$X_{s, w} \ge 0, \quad Y_{w, d} \ge 0, \quad U_d \ge 0$$

---

## 3. Solver Implementation

- **Engine**: Google OR-Tools Linear Solver (`pywraplp.Solver.CreateSolver('GLOP')`).
- **Complexity**: $20 \times 10 + 10 \times 30 + 30 = 530$ continuous variables and 70 linear constraints.
- **Compute Time**: Typically solved in **0.011 to 0.015 seconds**, making it fast enough for real-time interactive scenario simulation.

---

## 4. Empirical Baseline vs NEXUS Comparison

To validate that NEXUS generates measurable business value, every scenario compares the OR-Tools optimized solution against standard heuristic baseline operations (rigid primary supplier allocations without agile substitution).

### Benchmark Experiment: 80% Capacity Loss on Supplier `SUP_001` (Tata AutoComp) for 10 Days

| Metric | Baseline Heuristic Response | NEXUS Optimized Response | Empirical Impact / Value-Add |
| :--- | :---: | :---: | :---: |
| **Total Operational Cost** | INR 41,833,559.60 | **INR 19,291,240.54** | **-INR 22,542,319.06 (53.89% cost reduction)** |
| **Procurement Cost** | INR 11,817,420.00 | INR 12,845,900.00 | +INR 1,028,480.00 (Agile substitution) |
| **Transportation Freight** | INR 1,969,570.00 | INR 5,381,240.00 | Rerouting freight investment |
| **Shortage Penalty Incurred** | INR 26,238,450.00 | **INR 0.00** | **-INR 26,238,450.00 (100% penalties eliminated)** |
| **Total Unmet Shortage** | 74,967.0 units | **0.0 units** | **74,967 units saved** |
| **Network Service Level** | 51.24% | **100.00%** | **+48.76 percentage points** |
| **Solver Runtime** | N/A | **0.0114 seconds** | Real-time decision response |

### Analysis:
In the un-optimized baseline, the loss of Supplier `SUP_001` causes catastrophic stockouts at dependent warehouses because downstream zones are rigidly tied to local allocations. Unmet demand penalties explode (INR 26.2M), collapsing the service level to 51.24%.

In contrast, NEXUS dynamically reroutes procurement to secondary vendors (`SUP_005`, `SUP_009`, `SUP_010`) with available spare capacity. While freight and procurement costs rise modestly (+INR 4.4M), catastrophic penalty costs are completely averted, delivering a **net financial savings of INR 22.5M (53.89%)** and preserving a 100% service level.
