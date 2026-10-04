"""
NEXUS Supplier Risk Prediction Engine
Implements supervised risk classification comparing Logistic Regression baseline and XGBoost.
Evaluates Precision, Recall, F1, and ROC-AUC for imbalanced disruption failure detection.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from backend.app.config import settings
from backend.app.utils.logger import logger
from ml.evaluation.metrics import ModelEvaluator


class SupplierRiskModel:
    """
    Supervised predictive model to detect suppliers vulnerable to disruption or critical SLA breach.
    """

    FEATURE_COLS = [
        "on_time_rate",
        "average_delay",
        "delay_frequency",
        "quality_score",
        "lead_time",
        "lead_time_variability",
        "capacity_utilization",
        "historical_delays"
    ]

    def __init__(self, random_seed: int = settings.RANDOM_SEED):
        self.random_seed = random_seed
        self.model = None
        self.baseline_model = None
        self.metrics_summary = {}

    def train_and_evaluate(self, df_features: pd.DataFrame) -> Dict[str, Any]:
        """
        Trains Logistic Regression and XGBoost on supplier risk profiles, evaluates metrics.
        """
        logger.info(f"Training supplier risk prediction models on {len(df_features)} supplier records")
        X = df_features[self.FEATURE_COLS].values
        y = df_features["target_high_risk"].values.astype(int)

        # Out-of-sample evaluation: use GroupShuffleSplit by supplier_id if present
        if "supplier_id" in df_features.columns and len(df_features["supplier_id"].unique()) > 4:
            from sklearn.model_selection import GroupShuffleSplit
            gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=self.random_seed)
            train_idx, test_idx = next(gss.split(df_features, groups=df_features["supplier_id"]))
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            logger.info(f"Grouped train/test split: {len(np.unique(df_features['supplier_id'].iloc[train_idx]))} train suppliers, {len(np.unique(df_features['supplier_id'].iloc[test_idx]))} test suppliers")
        else:
            # Fallback to stratified split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.30, random_state=self.random_seed, stratify=y
            )

        # 1. Baseline Model: Logistic Regression
        lr = LogisticRegression(class_weight="balanced", random_state=self.random_seed, max_iter=500)
        lr.fit(X_train, y_train)
        y_pred_lr = lr.predict(X_test)
        y_prob_lr = lr.predict_proba(X_test)[:, 1] if hasattr(lr, "predict_proba") else y_pred_lr
        metrics_lr = ModelEvaluator.evaluate_classification(y_test, y_pred_lr, y_prob_lr)

        # 2. Advanced Model: XGBoost Classifier
        xgb = XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.08,
            scale_pos_weight=1.5,
            random_state=self.random_seed,
            eval_metric="logloss"
        )
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)
        y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
        metrics_xgb = ModelEvaluator.evaluate_classification(y_test, y_pred_xgb, y_prob_xgb)

        self.baseline_model = lr
        self.model = xgb

        # Feature Importance for explainability
        feat_imp = dict(zip(self.FEATURE_COLS, [round(float(x), 4) for x in xgb.feature_importances_]))
        sorted_imp = dict(sorted(feat_imp.items(), key=lambda x: x[1], reverse=True))

        self.metrics_summary = {
            "Logistic_Regression_Baseline": metrics_lr,
            "XGBoost_Risk_Classifier": metrics_xgb,
            "feature_importance": sorted_imp
        }

        logger.info(f"Supplier risk training complete. XGBoost F1: {metrics_xgb['f1_score']}, ROC-AUC: {metrics_xgb['roc_auc']}")
        return self.metrics_summary

    def predict_risk(self, feature_dict: Dict[str, float]) -> Dict[str, Any]:
        """
        Infers disruption probability and risk classification for a supplier.
        """
        if self.model is None:
            raise ValueError("Model is not loaded or trained.")

        vec = np.array([feature_dict[c] for c in self.FEATURE_COLS]).reshape(1, -1)
        prob = float(self.model.predict_proba(vec)[0, 1])
        prediction = int(self.model.predict(vec)[0])

        # Explain top risk driving factors
        top_risk_drivers = []
        if feature_dict.get("on_time_rate", 1.0) < 0.92:
            top_risk_drivers.append("Low on-time delivery reliability")
        if feature_dict.get("lead_time_variability", 0.0) > 1.0:
            top_risk_drivers.append("Excessive lead-time volatility")
        if feature_dict.get("capacity_utilization", 0.0) > 0.90:
            top_risk_drivers.append("Near-capacity strain (>90% utilization)")
        if feature_dict.get("historical_delays", 0) > 5:
            top_risk_drivers.append("Frequent historical shipment delays")

        return {
            "disruption_probability": round(prob, 4),
            "is_high_risk": bool(prediction == 1 or prob >= 0.35),
            "risk_tier": "CRITICAL" if prob >= 0.65 else ("HIGH" if prob >= 0.35 else "NORMAL"),
            "risk_drivers": top_risk_drivers or ["Standard operational variance"]
        }

    def save_model(self, model_dir: str = settings.MODEL_DIR):
        """Save model artifacts to disk."""
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        model_path = Path(model_dir) / "supplier_risk_model.joblib"
        meta_path = Path(model_dir) / "risk_metadata.json"

        joblib.dump({
            "model": self.model,
            "baseline_model": self.baseline_model,
            "feature_columns": self.FEATURE_COLS
        }, model_path)

        with open(meta_path, "w") as f:
            json.dump(self.metrics_summary, f, indent=2)

        logger.info(f"Supplier risk model and metrics saved to {model_dir}")

    def load_model(self, model_dir: str = settings.MODEL_DIR):
        """Load serialized model."""
        model_path = Path(model_dir) / "supplier_risk_model.joblib"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        bundle = joblib.load(model_path)
        self.model = bundle["model"]
        self.baseline_model = bundle["baseline_model"]
        logger.info(f"Loaded supplier risk model from {model_path}")
