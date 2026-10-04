# NEXUS Project Limitations & Academic Disclaimers

## 1. Academic Disclaimers

In accordance with B.Tech capstone academic evaluation principles:
1. **No Proprietary Commercial Affiliation**: All suppliers, production units, and warehouse entities represent simulated operations calibrated on authentic Indian geographic locations. They do NOT represent proprietary facilities or internal data of commercial entities.
2. **Hybrid Data Transparency**: Empirical demand volatility is derived from the Walmart Store Sales research dataset, and delivery delay distributions are calibrated from the DataCo Global Logistics dataset. Facility networks and multi-tier bills of materials are generated through a validated digital twin model. NEXUS never falsely claims synthetic data is real-world proprietary data.
3. **Simulation vs Deployment**: This implementation is an academic decision-intelligence prototype, tested and validated via simulated shocks, not a live production deployment inside an active enterprise ERP.

---

## 2. Technical & Modeling Limitations

### 2.1 Temporal Aggregation of Demand Data
- **Current State**: Empirical sales records are aggregated weekly, matching the cadence of the Walmart benchmark dataset.
- **Limitation**: Real-world e-commerce and retail supply chains experience hourly and daily order peaks.
- **Impact**: While weekly aggregation is ideal for strategic multi-week procurement, intraday warehouse picking bottlenecks are abstracted.

### 2.2 Linear vs Stochastic Optimization Formulation
- **Current State**: The optimization engine solves a deterministic continuous Linear Program (LP) using Google OR-Tools (`GLOP`).
- **Limitation**: In reality, customer demand, freight lead times, and diesel prices are stochastic variables subject to volatility distributions.
- **Impact**: While the current formulation solves within 0.015 seconds and generates globally optimal deterministic allocations, full stochastic programming with recourse would model risk distributions even more comprehensively.

### 2.3 Freight Cost and Transit Time Assumptions
- **Current State**: Highway distances are calculated using geodesic Haversine distance multiplied by an empirical Indian national highway winding factor of 1.22x. Transit speeds are fixed at 400 km/day for road freight and 550 km/day for rail freight.
- **Limitation**: Real-time road freight costs vary dynamically based on spot-market diesel prices, toll booth congestion, state border checkpoints, and seasonal monsoon conditions.

### 2.4 Scope of Multi-Tier Disruption Cascades
- **Current State**: NEXUS models disruption shocks across Tier-1 suppliers, warehouses, routes, and demand zones.
- **Limitation**: Tier-3 and Tier-4 raw material extraction nodes (e.g. semiconductor wafer foundries, bauxite mining) are not modeled in depth.

---

## 3. Recommended Future Roadmap

1. **Phase 2 (Frontend Layer)**:
   - Interactive React / Next.js supply chain control tower.
   - Mapbox / Leaflet geospatial map visualizing active Indian corridors, bottleneck nodes, and simulated disruption radii.
   - Interactive "What-If" scenario builder sliders for operations managers.
2. **Stochastic Optimization with Chance Constraints**:
   - Upgrading OR-Tools model to Mixed-Integer Linear Programming (MILP) with integer batch sizes and chance-constrained demand buffers.
3. **Real-Time Telemetry Integration**:
   - Integrating live GPS tracking from telematics APIs and OpenWeather disruption alerts.
4. **Natural Language Decision Explanations**:
   - Integrating Local LLM agents to conduct interactive conversational Q&A on why specific suppliers were chosen for emergency reallocation.
