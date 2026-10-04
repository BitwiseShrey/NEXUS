# NEXUS Scenario Simulation & Disruption Propagation Engine

## 1. Simulation Architecture

A central requirement of the NEXUS platform is **non-destructive scenario simulation**. Decision-makers must be able to explore "what-if" disruption hypotheses without mutating the underlying operational database.

```
       [Base Relational DB] ──(Deep Copy)──> [In-Memory SimulationState]
                                                      │
                                                      ├──> [Inject Shocks (Supplier/Route/Demand)]
                                                      ├──> [Graph Impact Propagation (NetworkX)]
                                                      ├──> [OR-Tools Optimization Solver]
                                                      └──> [Synthesize Recommendations]
```

---

## 2. Supported Disruption Scenarios

NEXUS models five distinct operational disruption scenarios:

### 2.1 Supplier Failure (`SUPPLIER_FAILURE`)
- **Parameters**: `supplier_id`, `capacity_reduction` (e.g., 0.80 = 80% loss), `duration_days`.
- **Mechanism**: Modifies the available capacity bound of the target supplier node, elevates its risk score to 0.85, and marks status as `DISRUPTED`.
- **Propagation**: Identifies dependent SKUs, down-stream warehouses, and triggers alternative supplier capacity discovery.

### 2.2 Route Disruption (`ROUTE_DISRUPTION`)
- **Parameters**: `route_id`, `duration_days`.
- **Mechanism**: Sets route status to `BLOCKED` and capacity to 0.0.
- **Propagation**: Uses NetworkX `shortest_simple_paths` to find feasible detours, calculating extra transit days and freight cost premiums.

### 2.3 Demand Spike (`DEMAND_SPIKE`)
- **Parameters**: `demand_spike_percent` (e.g., 0.70 = +70%), optional `zone_id`.
- **Mechanism**: Amplifies demand requirements across targeted or network-wide consumer zones.
- **Propagation**: Tests whether current safety stock and supplier capacity thresholds can absorb the surge without incurring stockout penalties.

### 2.4 Warehouse Shutdown (`WAREHOUSE_SHUTDOWN`)
- **Parameters**: `warehouse_id`, `duration_days`.
- **Mechanism**: Sets warehouse status to `SHUTDOWN`, capacity to 0.0, and automatically severs all inbound supplier routes and outbound distribution routes linked to this facility.
- **Propagation**: Calculates immobilized inventory and projects fulfillment deficits across regional feeder hubs.

### 2.5 Compound / Combined Disruption (`COMBINED_DISRUPTION`)
- **Parameters**: Simultaneous combinations of supplier cuts, severed transit routes, and regional demand surges (e.g., monsoon flood or regional cyclone event).
- **Mechanism**: Concurrently applies all individual shock transformations to stress-test the entire multi-echelon network.

---

## 3. Disruption Impact Propagation Algorithm

When an entity is disrupted, the `ImpactEngine` executes multi-echelon dependency traversal:

1. **Product Dependency**: Identifies all SKUs where `primary_supplier_id == entity_id`.
2. **Facility Dependency**: Identifies all downstream warehouses receiving goods from the disrupted node.
3. **Inventory Runway Calculation**:
   $$\text{Runway (Days)} = \frac{\text{Current Stock}}{\text{Average Daily Demand}}$$
   If $\text{Runway} < \text{Disruption Duration}$, a stockout breach is flagged.
4. **Shortage Estimation**:
   $$\text{Lost Capacity} = \text{Capacity} \times \text{Capacity Reduction} \times \left(\frac{\text{Duration}}{30}\right)$$
5. **Projected Service-Level Drop**:
   $$\Delta \text{SL} = \min\left(0.35, \frac{\text{Lost Capacity}}{\text{Daily Demand} \times \text{Duration}} \times 0.25\right)$$
   $$\text{Projected SL} = \max(0.60, \text{Baseline SL} - \Delta \text{SL})$$

The simulation output provides the exact boundary conditions used by the OR-Tools optimization engine to compute the optimal recovery plan.
