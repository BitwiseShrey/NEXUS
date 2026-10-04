"""
NEXUS Recommendation Engine
Translates raw model risk probabilities, impact propagation, and OR-Tools optimization solutions
into plain-language, executive-actionable supply chain decisions.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import OptimizationRun, Recommendation
from backend.app.utils.logger import logger


class RecommendationEngine:
    """
    Transforms quantitative optimization and simulation outputs into explainable business decisions.
    """

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def generate_recommendation(
        self,
        scenario_name: str,
        impact_result: Dict[str, Any],
        comparison_result: Dict[str, Any],
        persist: bool = True
    ) -> Dict[str, Any]:
        """
        Synthesizes impact and optimization solutions into a formal recommendation.
        """
        baseline = comparison_result.get("baseline", {})
        nexus = comparison_result.get("nexus_optimized", {})
        comp = comparison_result.get("impact_comparison", {})

        cost_saved = comp.get("cost_saved_inr", 0.0)
        cost_saved_pct = comp.get("cost_reduction_percent", 0.0)
        shortage_avoided = comp.get("shortage_reduction_units", 0.0)
        sl_gain = comp.get("service_level_improvement_percentage_points", 0.0)

        disrupted_entity = impact_result.get("disrupted_entity", {})
        entity_name = disrupted_entity.get("name", "Key Network Facility")
        entity_id = disrupted_entity.get("id", "FACILITY")
        duration = disrupted_entity.get("duration_days", 10)

        # Build dynamic reallocation advice based on top OR-Tools allocations
        top_allocations = nexus.get("top_allocations", [])
        sup_allocs = [a for a in top_allocations if a["type"] == "SUPPLIER_TO_WAREHOUSE"]

        actions = []
        if sup_allocs:
            tot_sup_units = sum([a["units"] for a in sup_allocs])
            for alloc in sup_allocs[:3]:
                pct = (alloc["units"] / max(tot_sup_units, 1.0)) * 100
                actions.append(f"Shift {pct:.1f}% ({alloc['units']:.0f} units) of demand to {alloc['from']}")
        else:
            actions.append("Rebalance regional warehouse safety stocks across unaffected hubs.")

        title = f"Mitigation Strategy for {entity_name} Disruption ({scenario_name})"

        reason = (
            f"Risk analysis detected that {entity_name} ({entity_id}) faces significant capacity degradation "
            f"over a projected {duration}-day window. Without intervention, baseline heuristic operations "
            f"would cause a shortage of {baseline.get('total_shortages', 0.0):,.1f} units, dropping network "
            f"service levels to {baseline.get('service_level', 0.0)*100:.1f}%."
        )

        expected_benefit = (
            f"Adopting the NEXUS optimized multi-echelon allocation reduces network shortage by "
            f"{shortage_avoided:,.1f} units, maintains service level at {nexus.get('service_level', 0.0)*100:.1f}% "
            f"(+{sl_gain}% vs baseline), and achieves net operational savings of INR {cost_saved:,.2f} ({cost_saved_pct}% cost reduction)."
        )

        affected_entities = {
            "primary_disrupted_entity": entity_id,
            "dependent_products": impact_result.get("dependent_products", [])[:5],
            "affected_warehouses": impact_result.get("affected_warehouses_count", 0),
            "affected_demand_zones": impact_result.get("affected_demand_zones", [])[:5]
        }

        # Mathematically derived Plan Feasibility & Robustness Index:
        # Evaluates solver optimality, service level preservation, and shortage mitigation fraction
        is_optimal = 1.0 if nexus.get("status") == "OPTIMAL" else 0.70
        sl = float(nexus.get("service_level", 1.0))
        base_shortage = max(float(baseline.get("total_shortages", 1.0)), 1.0)
        shortage_mitigation = min(1.0, max(0.0, float(shortage_avoided) / base_shortage))
        plan_robustness_score = round(float(is_optimal * (0.55 * sl + 0.45 * shortage_mitigation)), 3)
        plan_robustness_score = min(0.98, max(0.50, plan_robustness_score))

        run_id = f"RUN_{uuid.uuid4().hex[:8].upper()}"
        rec_id = f"REC_{uuid.uuid4().hex[:8].upper()}"

        rec_payload = {
            "recommendation_id": rec_id,
            "run_id": run_id,
            "title": title,
            "reason": reason,
            "recommended_actions": actions,
            "affected_entities": affected_entities,
            "action_type": "REALLOCATE_AND_REROUTE",
            "expected_benefit": expected_benefit,
            "expected_cost": nexus.get("total_cost", 0.0),
            "cost_saved_inr": cost_saved,
            "confidence_score": plan_robustness_score,
            "created_at": datetime.utcnow().isoformat()
        }

        # Persist to database if requested
        if persist:
            try:
                opt_run = OptimizationRun(
                    run_id=run_id,
                    scenario_name=scenario_name,
                    objective_type="MINIMIZE_TOTAL_COST",
                    status=nexus.get("status", "OPTIMAL"),
                    total_cost=nexus.get("total_cost", 0.0),
                    service_level=nexus.get("service_level", 0.0),
                    shortages_total=nexus.get("total_shortages", 0.0),
                    procurement_cost=nexus.get("procurement_cost", 0.0),
                    transportation_cost=nexus.get("transportation_cost", 0.0),
                    penalty_cost=nexus.get("penalty_cost", 0.0),
                    runtime_seconds=nexus.get("runtime_seconds", 0.0)
                )
                self.db.add(opt_run)

                rec_orm = Recommendation(
                    recommendation_id=rec_id,
                    run_id=run_id,
                    title=title,
                    reason=reason,
                    affected_entities=affected_entities,
                    action_type="REALLOCATE_AND_REROUTE",
                    expected_benefit=expected_benefit,
                    expected_cost=nexus.get("total_cost", 0.0),
                    confidence_score=0.94
                )
                self.db.add(rec_orm)
                self.db.commit()
                logger.info(f"Persisted recommendation {rec_id} for run {run_id}")
            except Exception as e:
                self.db.rollback()
                logger.error(f"Failed to persist recommendation: {e}")

        return rec_payload
