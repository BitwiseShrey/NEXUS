"""
Unit Tests for NEXUS Supplier Risk Prediction and Unified Risk Engine
"""

import pandas as pd
import numpy as np
from ml.risk.supplier_risk_model import SupplierRiskModel
from ml.evaluation.metrics import ModelEvaluator
from digital_twin.risk_engine import UnifiedRiskEngine
from backend.app.models import Supplier


def test_classification_metrics():
    y_true = np.array([1, 0, 1, 1, 0])
    y_pred = np.array([1, 0, 1, 0, 0])
    y_prob = np.array([0.9, 0.1, 0.8, 0.4, 0.2])
    metrics = ModelEvaluator.evaluate_classification(y_true, y_pred, y_prob)

    assert metrics["precision"] == 1.0
    assert metrics["recall"] == round(2 / 3, 4)
    assert metrics["roc_auc"] > 0.5


def test_supplier_risk_model_workflow():
    # Synthetic test dataset
    n_samples = 80
    data = {
        "on_time_rate": np.random.uniform(0.70, 0.99, n_samples),
        "average_delay": np.random.uniform(0.5, 6.0, n_samples),
        "delay_frequency": np.random.uniform(0.01, 0.30, n_samples),
        "quality_score": np.random.uniform(0.80, 0.99, n_samples),
        "lead_time": np.random.uniform(2.0, 8.0, n_samples),
        "lead_time_variability": np.random.uniform(0.2, 2.5, n_samples),
        "capacity_utilization": np.random.uniform(0.60, 0.98, n_samples),
        "historical_delays": np.random.randint(0, 15, n_samples),
    }
    # Deterministic high risk rule for test
    df = pd.DataFrame(data)
    df["target_high_risk"] = ((df["on_time_rate"] < 0.90) | (df["historical_delays"] > 7)).astype(int)

    model = SupplierRiskModel(random_seed=42)
    eval_res = model.train_and_evaluate(df)

    assert "XGBoost_Risk_Classifier" in eval_res
    assert "Logistic_Regression_Baseline" in eval_res
    assert eval_res["XGBoost_Risk_Classifier"]["roc_auc"] >= 0.70

    # Test single prediction
    pred = model.predict_risk({
        "on_time_rate": 0.82,
        "average_delay": 4.5,
        "delay_frequency": 0.18,
        "quality_score": 0.89,
        "lead_time": 6.0,
        "lead_time_variability": 2.1,
        "capacity_utilization": 0.95,
        "historical_delays": 11
    })
    assert "disruption_probability" in pred
    assert pred["is_high_risk"] is True
    assert len(pred["risk_drivers"]) > 0


def test_unified_risk_supplier_scoring():
    # Test explainable calculation
    engine = UnifiedRiskEngine()
    sup = Supplier(
        supplier_id="SUP_TEST",
        supplier_name="Test Supplier",
        on_time_rate=0.85,
        quality_score=0.92,
        lead_time=5.0,
        historical_delays=6,
        capacity=10000.0,
        risk_score=0.25
    )
    score_dict = engine.evaluate_supplier_risk(sup)
    assert 0.05 <= score_dict["risk_score"] <= 0.95
    assert len(score_dict["drivers"]) > 0
