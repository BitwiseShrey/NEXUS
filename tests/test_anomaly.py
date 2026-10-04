"""
Unit Tests for NEXUS Isolation Forest Anomaly Detection
"""

import pandas as pd
import numpy as np
from ml.anomaly.isolation_forest_detector import AnomalyDetector


def test_anomaly_detector_training_and_detection():
    # Generate mostly normal orders + a few blatant outliers
    normal_data = {
        "order_id": [f"ORD_{i}" for i in range(100)],
        "quantity": np.random.normal(25.0, 5.0, 100),
        "is_late": np.zeros(100),
        "lead_time_deviation": np.zeros(100)
    }
    df_normal = pd.DataFrame(normal_data)

    outliers = pd.DataFrame({
        "order_id": ["ORD_SPIKE_1", "ORD_DELAY_1"],
        "quantity": [500.0, 30.0],
        "is_late": [0, 1],
        "lead_time_deviation": [0.0, 12.0]
    })

    df_all = pd.concat([df_normal, outliers], ignore_index=True)

    detector = AnomalyDetector(contamination=0.05, random_seed=42)
    detector.fit(df_all)

    # Test detection on outliers
    anomalies = detector.detect_anomalies(outliers)
    assert len(anomalies) > 0
    types = [a["anomaly_type"] for a in anomalies]
    assert "UNUSUAL_DEMAND_SPIKE" in types or "TRANSIT_DELAY_OUTLIER" in types
