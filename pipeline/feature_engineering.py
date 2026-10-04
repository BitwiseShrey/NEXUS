"""
NEXUS Feature Engineering Engine
Transforms time-series demand, supplier performance metrics, and operational logs into ML features.
"""

from typing import Tuple
import pandas as pd
import numpy as np
from backend.app.utils.logger import logger


class FeatureEngineer:
    """
    Constructs reproducible feature matrices for forecasting, risk prediction, and anomaly detection.
    """

    @staticmethod
    def create_forecasting_features(
        df_series: pd.DataFrame,
        target_col: str = "demand",
        date_col: str = "date"
    ) -> pd.DataFrame:
        """
        Creates time-series lag and rolling statistics features.
        df_series should contain [date, demand] sorted chronologically.
        """
        df = df_series.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(by=date_col).reset_index(drop=True)

        # Calendar features
        df["month"] = df[date_col].dt.month
        df["week"] = df[date_col].dt.isocalendar().week.astype(int)
        df["quarter"] = df[date_col].dt.quarter
        df["day_of_year"] = df[date_col].dt.dayofyear
        df["trend"] = np.arange(len(df))

        # Autoregressive Lag Features
        df["lag_1"] = df[target_col].shift(1)
        df["lag_2"] = df[target_col].shift(2)
        df["lag_4"] = df[target_col].shift(4)
        df["lag_8"] = df[target_col].shift(8)

        # Rolling Window Statistics (avoiding lookahead bias by shifting 1 step)
        df["rolling_mean_4"] = df[target_col].shift(1).rolling(window=4, min_periods=1).mean()
        df["rolling_std_4"] = df[target_col].shift(1).rolling(window=4, min_periods=1).std().fillna(0)
        df["rolling_mean_8"] = df[target_col].shift(1).rolling(window=8, min_periods=1).mean()
        df["rolling_max_4"] = df[target_col].shift(1).rolling(window=4, min_periods=1).max()
        df["rolling_min_4"] = df[target_col].shift(1).rolling(window=4, min_periods=1).min()

        # Drop warmup rows where lag_8 is NaN
        df_clean = df.dropna().reset_index(drop=True)
        return df_clean

    @staticmethod
    def create_supplier_risk_features(suppliers: list, historical_orders: list = None) -> pd.DataFrame:
        """
        Extracts multi-dimensional supplier risk profiles.
        Features:
        - on_time_rate
        - average_delay
        - delay_frequency
        - quality_score
        - lead_time
        - lead_time_variability
        - capacity_utilization
        - historical_delays
        Target: target_high_risk (Independent binary disruption / SLA breach event based on latent operational strain + stochastic shock)
        """
        records = []
        for s in suppliers:
            # Baseline capability metrics
            otr = float(s.get("on_time_rate", 0.95))
            qs = float(s.get("quality_score", 0.98))
            lt = float(s.get("lead_time", 4.0))
            cap = float(s.get("capacity", 15000.0))
            hist_delays = int(s.get("historical_delays", 0))
            risk_score = float(s.get("risk_score", 0.1))

            # Variance calibrated
            lt_var = float(s.get("lead_time_variability", round(lt * (1.0 - otr) * 1.5, 2)))
            avg_delay = float(s.get("average_delay", round((1.0 - otr) * 3.5, 2)))
            delay_freq = float(s.get("delay_frequency", round(1.0 - otr, 3)))
            cap_util = float(s.get("capacity_utilization", round(min(0.85 + (risk_score * 0.15), 0.99), 2)))

            # Latent operational stress DGP:
            # Failure is an independent forward event resulting from multi-factor stress + stochastic shock
            latent_strain = (
                2.4 * (1.0 - otr) +
                1.8 * (1.0 - qs) +
                0.12 * (lt / 10.0) +
                1.1 * (lt_var / 3.0) +
                1.4 * max(cap_util - 0.85, 0.0) +
                0.08 * min(hist_delays, 6) -
                0.95
            )
            shock = float(s.get("stochastic_shock", np.random.normal(0, 0.35)))
            disruption_prob = 1.0 / (1.0 + np.exp(-(latent_strain + shock)))
            target = 1 if disruption_prob >= 0.50 else 0

            records.append({
                "supplier_id": s.get("supplier_id", "SUP_001"),
                "on_time_rate": otr,
                "average_delay": avg_delay,
                "delay_frequency": delay_freq,
                "quality_score": qs,
                "lead_time": lt,
                "lead_time_variability": lt_var,
                "capacity_utilization": cap_util,
                "historical_delays": hist_delays,
                "target_high_risk": target,
                "continuous_risk_score": risk_score
            })

        return pd.DataFrame(records)

    @staticmethod
    def create_anomaly_detection_features(orders: list) -> pd.DataFrame:
        """
        Features for Isolation Forest unsupervised anomaly detection.
        Features: order quantity, transit delay days, order velocity.
        """
        rows = []
        for ord_item in orders:
            qty = float(ord_item["quantity"])
            status = ord_item.get("status", "DELIVERED")
            is_late = 1.0 if status == "LATE" else 0.0
            rows.append({
                "order_id": ord_item["order_id"],
                "quantity": qty,
                "is_late": is_late,
                "quantity_z": qty  # will be scaled in pipeline
            })
        return pd.DataFrame(rows)
