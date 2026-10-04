"""
NEXUS Anomaly Detection Engine
Uses Isolation Forest to detect multi-signal operational anomalies:
- Demand surges
- Delivery delays
- Abnormal order volumes
- Lead-time deviations
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from backend.app.config import settings
from backend.app.utils.logger import logger


class AnomalyDetector:
    """
    Unsupervised multi-variate anomaly detector for supply chain disruptions.
    """

    def __init__(self, contamination: float = 0.03, random_seed: int = settings.RANDOM_SEED):
        self.contamination = contamination
        self.random_seed = random_seed
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_seed,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.feature_names = ["quantity", "is_late", "lead_time_deviation"]

    def fit(self, df_records: pd.DataFrame):
        """
        Fits scaler and Isolation Forest on supply chain operational records.
        """
        logger.info(f"Fitting Isolation Forest on {len(df_records)} operational events")
        df = df_records.copy()
        if "lead_time_deviation" not in df.columns:
            df["lead_time_deviation"] = 0.0

        X = df[self.feature_names].fillna(0.0).values
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        logger.info("Isolation Forest fitted successfully.")
        return self

    def detect_anomalies(self, df_events: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Scores events and identifies outliers.
        Returns list of structured anomaly signals.
        """
        df = df_events.copy()
        if "lead_time_deviation" not in df.columns:
            df["lead_time_deviation"] = 0.0

        X = df[self.feature_names].fillna(0.0).values
        X_scaled = self.scaler.transform(X)

        # -1 = anomaly, 1 = normal
        preds = self.model.predict(X_scaled)
        scores = self.model.decision_function(X_scaled)

        anomalies = []
        for i, (pred, raw_score) in enumerate(zip(preds, scores)):
            if pred == -1:  # Anomaly detected
                row = df.iloc[i]
                qty = float(row.get("quantity", 0.0))
                is_late = bool(row.get("is_late", 0))
                lt_dev = float(row.get("lead_time_deviation", 0.0))

                # Deduce anomaly type
                if qty > 50:
                    atype = "UNUSUAL_DEMAND_SPIKE"
                elif is_late or lt_dev > 3.0:
                    atype = "TRANSIT_DELAY_OUTLIER"
                else:
                    atype = "ORDER_PATTERN_ANOMALY"

                # Severity: convert decision score (negative) to 0.0 - 1.0 range
                severity = round(float(np.clip(-raw_score * 2.5, 0.2, 0.99)), 3)

                anomalies.append({
                    "entity": str(row.get("order_id", f"EVT_{i}")),
                    "anomaly_type": atype,
                    "severity": severity,
                    "score": round(float(raw_score), 4),
                    "timestamp": datetime.utcnow().isoformat(),
                    "details": {
                        "quantity": qty,
                        "is_late": is_late,
                        "lead_time_deviation": lt_dev
                    }
                })

        logger.info(f"Anomaly detection scan identified {len(anomalies)} anomalies out of {len(df_events)} events.")
        return anomalies

    def save_model(self, model_dir: str = settings.MODEL_DIR):
        """Save model and scaler to disk."""
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        path = Path(model_dir) / "anomaly_model.joblib"
        joblib.dump({"model": self.model, "scaler": self.scaler, "features": self.feature_names}, path)
        logger.info(f"Saved anomaly detector to {path}")

    def load_model(self, model_dir: str = settings.MODEL_DIR):
        """Load model from disk."""
        path = Path(model_dir) / "anomaly_model.joblib"
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at {path}")
        bundle = joblib.load(path)
        self.model = bundle["model"]
        self.scaler = bundle["scaler"]
        self.feature_names = bundle["features"]
        logger.info(f"Loaded anomaly detector from {path}")
