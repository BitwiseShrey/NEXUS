"""
NEXUS End-to-End Decision Intelligence Demonstration Pipeline
Orchestrates the complete 12-stage workflow:
Ingest -> Validate -> Forecast -> Predict Risk -> Detect Anomalies -> Graph Topology ->
Simulate Disruption -> Propagate Impact -> OR-Tools Optimize -> Compare with Baseline ->
Synthesize Recommendation -> Persist Audit Trail
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
from datetime import datetime
from backend.app.config import settings
from backend.app.database import SessionLocal, init_db
from backend.app.models import (
    Supplier, Warehouse, Route, DemandZone, Product, ProductionUnit, DistributionHub
)
from backend.app.utils.logger import logger
from digital_twin.analytics import SupplyChainAnalytics
from digital_twin.network_graph import SupplyChainGraph
from digital_twin.risk_engine import UnifiedRiskEngine
from impact.impact_engine import ImpactEngine
from ml.anomaly.isolation_forest_detector import AnomalyDetector
from ml.forecasting.xgboost_forecaster import DemandForecaster
from ml.risk.supplier_risk_model import SupplierRiskModel
from optimization.ortools_optimizer import SupplyChainOptimizer
from pipeline.data_ingestion import run_ingestion
from pipeline.feature_engineering import FeatureEngineer
from pipeline.train_models import run_training
from recommendation.recommendation_engine import RecommendationEngine
from simulation.scenario_engine import ScenarioEngine, ScenarioType


def run_complete_nexus_pipeline():
    print("=" * 75)
    print(" NEXUS: AI-POWERED SUPPLY CHAIN INTELLIGENCE & OPTIMIZATION PLATFORM ")
    print("=" * 75)
    start_time = datetime.utcnow()

    # Step 1 & 2: Data Ingestion, Digital Twin Generation, & Validation
    logger.info("[STAGE 1/11] Running Data Ingestion & Digital Twin Network Generation...")
    ingestion_summary = run_ingestion()
    logger.info(f"Ingested {ingestion_summary['orders_count']} orders across {ingestion_summary['suppliers_count']} suppliers and {ingestion_summary['warehouses_count']} warehouses.")

    # Step 3: Model Training & Artifact Generation
    logger.info("[STAGE 2/11] Verifying & Training Machine Learning Models...")
    ml_results = run_training()
    best_fc = ml_results["forecasting"]["winner_model"]
    fc_rmse = ml_results["forecasting"]["evaluation_metrics"][best_fc]["RMSE"]
    logger.info(f"Forecasting benchmark winner: {best_fc} (RMSE: {fc_rmse:,.2f})")

    db = SessionLocal()
    try:
        # Step 4: Baseline Operational Analytics
        logger.info("[STAGE 3/11] Calculating Baseline Operational KPIs...")
        analytics = SupplyChainAnalytics(db)
        kpis = analytics.get_network_executive_summary()
        logger.info(f"Active Suppliers: {kpis['suppliers']['total_suppliers']}, Mean On-Time: {kpis['suppliers']['mean_on_time_rate']*100:.1f}%")
        logger.info(f"Inventory Valuation: INR {kpis['inventory']['total_inventory_valuation_inr']:,.2f}, Total Corridors: {kpis['routes']['total_routes']}")

        # Step 5: Multi-dimensional Unified Risk Profile
        logger.info("[STAGE 4/11] Computing Unified Supply Chain Risk Profile...")
        risk_engine = UnifiedRiskEngine(db)
        network_risk = risk_engine.compute_network_risk_profile()
        logger.info(f"Composite Network Risk Score: {network_risk['composite_network_risk_score']} [{network_risk['risk_status']}]")

        # Step 6: Network Topology Graph Construction
        logger.info("[STAGE 5/11] Building NetworkX Multi-Echelon Directed Graph...")
        graph = SupplyChainGraph()
        sups = [{k: v for k, v in s.__dict__.items() if k != "_sa_instance_state"} for s in db.query(Supplier).all()]
        prods = [{k: v for k, v in p.__dict__.items() if k != "_sa_instance_state"} for p in db.query(ProductionUnit).all()]
        whs = [{k: v for k, v in w.__dict__.items() if k != "_sa_instance_state"} for w in db.query(Warehouse).all()]
        hubs = [{k: v for k, v in h.__dict__.items() if k != "_sa_instance_state"} for h in db.query(DistributionHub).all()]
        routes = [{k: v for k, v in r.__dict__.items() if k != "_sa_instance_state"} for r in db.query(Route).all()]
        dzs = [{k: v for k, v in d.__dict__.items() if k != "_sa_instance_state"} for d in db.query(DemandZone).all()]

        graph.build_from_entities(
            suppliers=sups,
            production_units=prods,
            warehouses=whs,
            hubs=hubs,
            demand_zones=dzs,
            routes=routes
        )
        centrality = graph.compute_network_criticality()
        top_critical_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
        logger.info(f"Network graph topology: {graph.graph.number_of_nodes()} nodes, {graph.graph.number_of_edges()} edges. Top critical nodes: {top_critical_nodes}")

        # Step 7: Inject Disruption Shock Scenario
        target_supplier_id = "SUP_001"
        logger.info(f"[STAGE 6/11] Injecting Disruption Scenario: 80% Capacity Loss on Supplier {target_supplier_id} for 10 Days...")
        scenario_engine = ScenarioEngine(db)
        sim_res = scenario_engine.run_scenario(
            ScenarioType.SUPPLIER_FAILURE,
            {"supplier_id": target_supplier_id, "capacity_reduction": 0.80, "duration_days": 10}
        )
        sim_state = sim_res["state_object"]
        logger.info(f"Simulated network state: Total demand = {sim_res['simulated_network_state']['total_demand_units']} units, Net capacity balance = {sim_res['simulated_network_state']['net_capacity_balance']} units.")

        # Step 8: Disruption Impact Propagation
        logger.info(f"[STAGE 7/11] Propagating Impact across Supply Chain Graph...")
        impact_engine = ImpactEngine(sc_graph=graph, db=db)
        impact_res = impact_engine.analyze_supplier_disruption(
            supplier_id=target_supplier_id,
            capacity_reduction=0.80,
            duration_days=10
        )
        logger.info(f"Impact Analysis: {impact_res['dependent_products_count']} products exposed, Projected Shortage: {impact_res['estimated_shortage_units']} units.")
        logger.info(f"Service Level: Projected to drop from {impact_res['baseline_service_level']*100:.1f}% to {impact_res['projected_service_level']*100:.1f}% (-{impact_res['service_level_deficit']*100:.1f}%).")

        # Step 9: Multi-Echelon Optimization (Google OR-Tools)
        logger.info("[STAGE 8/11] Running Google OR-Tools Multi-Echelon Allocation Model...")
        optimizer = SupplyChainOptimizer(risk_aversion_weight=50.0, shortage_penalty_unit=350.0)
        comparison = optimizer.compare_with_baseline(sim_state)

        # Step 10: Baseline vs NEXUS Empirical Comparison
        logger.info("[STAGE 9/11] Evaluating Baseline vs NEXUS Performance...")
        comp = comparison["impact_comparison"]
        logger.info("-------------------------------------------------------------")
        logger.info(f"Baseline Response Total Cost:  INR {comparison['baseline']['total_cost']:,.2f}")
        logger.info(f"NEXUS Optimized Total Cost:     INR {comparison['nexus_optimized']['total_cost']:,.2f}")
        logger.info(f"Net Financial Savings:          INR {comp['cost_saved_inr']:,.2f} ({comp['cost_reduction_percent']}%)")
        logger.info(f"Unmet Shortage Units Avoided:   {comp['shortage_reduction_units']:,.1f} units")
        logger.info(f"Service Level Improvement:      +{comp['service_level_improvement_percentage_points']}%")
        logger.info("-------------------------------------------------------------")

        # Step 11: Actionable Recommendation Generation & Audit Trail
        logger.info("[STAGE 10/11] Synthesizing Explainable Executive Recommendation...")
        rec_engine = RecommendationEngine(db)
        recommendation = rec_engine.generate_recommendation(
            scenario_name=f"SUPPLIER_FAILURE [{target_supplier_id}]",
            impact_result=impact_res,
            comparison_result=comparison,
            persist=True
        )
        logger.info(f"Recommendation Generated [{recommendation['recommendation_id']}]: {recommendation['title']}")
        logger.info(f"Rationale: {recommendation['reason']}")
        logger.info(f"Action Items: {recommendation['recommended_actions']}")

        # Step 12: Write Execution Demonstration Artifact
        logger.info("[STAGE 11/11] Writing Final Pipeline Demonstration Artifact...")
        runtime_sec = round((datetime.utcnow() - start_time).total_seconds(), 2)

        demo_report = {
            "platform": "NEXUS Supply Chain Decision Intelligence Platform",
            "execution_timestamp": datetime.utcnow().isoformat(),
            "runtime_seconds": runtime_sec,
            "status": "ALL_STAGES_COMPLETED_SUCCESSFULLY",
            "digital_twin": ingestion_summary,
            "machine_learning": {
                "demand_forecasting_winner": best_fc,
                "demand_forecasting_rmse": fc_rmse,
                "supplier_risk_f1": ml_results["supplier_risk"]["XGBoost_Risk_Classifier"]["f1_score"],
                "supplier_risk_auc": ml_results["supplier_risk"]["XGBoost_Risk_Classifier"]["roc_auc"],
                "anomalies_detected": ml_results["anomaly_detection"]["sample_anomalies_detected"]
            },
            "disruption_scenario": {
                "type": "SUPPLIER_FAILURE",
                "entity": target_supplier_id,
                "capacity_cut": "80%",
                "duration": "10 days"
            },
            "impact_analysis": {
                "products_at_risk": impact_res["dependent_products_count"],
                "shortage_risk_units": impact_res["estimated_shortage_units"],
                "baseline_service_level": impact_res["baseline_service_level"],
                "projected_service_level": impact_res["projected_service_level"]
            },
            "optimization_gain": comp,
            "recommendation": recommendation
        }

        output_path = Path("docs/demo_execution_report.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(demo_report, f, indent=2)

        print("\n" + "=" * 75)
        print(" NEXUS PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN " + str(runtime_sec) + "s ")
        print(f" Summary Report saved to: {output_path}")
        print("=" * 75 + "\n")
        return demo_report

    finally:
        db.close()


if __name__ == "__main__":
    run_complete_nexus_pipeline()
