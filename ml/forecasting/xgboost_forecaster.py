"""
NEXUS Demand Forecasting Engine
Implements lag-engineered XGBoost Regressor, automated baseline benchmarking,
time-based validation splitting, and model persistence.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd
import joblib
from xgboost import XGBRegressor

from backend.app.config import settings
from backend.app.utils.logger import logger
from ml.evaluation.metrics import ModelEvaluator
from ml.forecasting.baseline_models import NaiveForecaster, MovingAverageForecaster
from pipeline.feature_engineering import FeatureEngineer


class DemandForecaster:
    """
    Automated multi-model demand forecasting system.
    Evaluates Naive, Moving Average, and XGBoost on chronologically held-out test data.
    """

    def __init__(self, random_seed: int = settings.RANDOM_SEED):
        self.random_seed = random_seed
        self.best_model_name = None
        self.model = None
        self.feature_columns = None
        self.metrics_summary = {}

    def prepare_data(
        self,
        df_series: pd.DataFrame,
        target_col: str = "demand",
        date_col: str = "date"
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list]:
        """
        Creates lag features and applies strict chronological time-series split:
        Train: 70%, Validation: 15%, Test: 15%
        """
        df_feat = FeatureEngineer.create_forecasting_features(df_series, target_col, date_col)
        n = len(df_feat)
        train_idx = int(n * 0.70)
        val_idx = int(n * 0.85)

        train_df = df_feat.iloc[:train_idx].copy()
        val_df = df_feat.iloc[train_idx:val_idx].copy()
        test_df = df_feat.iloc[val_idx:].copy()

        feature_cols = [
            "month", "week", "quarter", "day_of_year", "trend",
            "lag_1", "lag_2", "lag_4", "lag_8",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_8",
            "rolling_max_4", "rolling_min_4"
        ]
        self.feature_columns = feature_cols

        return train_df, val_df, test_df, feature_cols

    def train_and_benchmark(
        self,
        df_series: pd.DataFrame,
        target_col: str = "demand",
        date_col: str = "date"
    ) -> Dict[str, Any]:
        """
        Trains baseline models and XGBoost, evaluates on test set, and selects the winner.
        """
        logger.info(f"Initiating demand forecasting training pipeline on {len(df_series)} observations")
        train_df, val_df, test_df, feature_cols = self.prepare_data(df_series, target_col, date_col)

        X_train, y_train = train_df[feature_cols].values, train_df[target_col].values
        X_val, y_val = val_df[feature_cols].values, val_df[target_col].values
        X_test, y_test = test_df[feature_cols].values, test_df[target_col].values

        # 1. Benchmark: Naive Forecaster
        naive_model = NaiveForecaster()
        naive_model.fit(y_train)
        y_pred_naive = np.full(len(y_test), naive_model.last_value)
        metrics_naive = ModelEvaluator.evaluate_regression(y_test, y_pred_naive)

        # 2. Benchmark: 4-week Moving Average
        ma4_model = MovingAverageForecaster(window=4)
        ma4_model.fit(y_train)
        y_pred_ma4 = np.full(len(y_test), ma4_model.mean_value)
        metrics_ma4 = ModelEvaluator.evaluate_regression(y_test, y_pred_ma4)

        # 3. Benchmark: 8-week Moving Average
        ma8_model = MovingAverageForecaster(window=8)
        ma8_model.fit(y_train)
        y_pred_ma8 = np.full(len(y_test), ma8_model.mean_value)
        metrics_ma8 = ModelEvaluator.evaluate_regression(y_test, y_pred_ma8)

        # 4. Machine Learning: XGBoost Regressor
        xgb = XGBRegressor(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=self.random_seed,
            n_jobs=-1
        )
        xgb.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )

        y_pred_xgb = xgb.predict(X_test)
        # Ensure predicted demands cannot be physically negative
        y_pred_xgb = np.maximum(y_pred_xgb, 0.0)
        metrics_xgb = ModelEvaluator.evaluate_regression(y_test, y_pred_xgb)

        # Store model comparison
        comparison = {
            "Naive": metrics_naive,
            "MovingAverage_4W": metrics_ma4,
            "MovingAverage_8W": metrics_ma8,
            "XGBoost_Regressor": metrics_xgb
        }

        # Automated selection based on minimum RMSE
        best_name = min(comparison.keys(), key=lambda k: comparison[k]["RMSE"])
        self.best_model_name = best_name
        self.model = xgb
        self.metrics_summary = comparison

        logger.info(f"Model evaluation completed. Winner: {best_name} (RMSE: {comparison[best_name]['RMSE']})")
        logger.info(f"Benchmark summary: {comparison}")

        # Feature importances for explainability
        importances = dict(zip(feature_cols, [round(float(x), 4) for x in xgb.feature_importances_]))
        sorted_importance = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))

        result = {
            "winner_model": best_name,
            "evaluation_metrics": comparison,
            "feature_importance": sorted_importance,
            "training_samples": len(train_df),
            "test_samples": len(test_df)
        }
        return result

    def forecast_future(self, df_recent: pd.DataFrame, horizon_steps: int = 12) -> List[float]:
        """
        Recursively generates future demand forecasts for specified horizon.
        """
        if self.model is None:
            raise ValueError("Model is not trained. Call train_and_benchmark or load first.")

        history = df_recent["demand"].tolist()
        last_date = pd.to_datetime(df_recent["date"].iloc[-1])
        forecasts = []

        current_date = last_date
        for step in range(1, horizon_steps + 1):
            current_date += pd.Timedelta(weeks=1)

            # Reconstruct feature vector from history
            lag_1 = history[-1]
            lag_2 = history[-2] if len(history) >= 2 else lag_1
            lag_4 = history[-4] if len(history) >= 4 else lag_1
            lag_8 = history[-8] if len(history) >= 8 else lag_1

            roll_4 = np.mean(history[-4:]) if len(history) >= 4 else lag_1
            roll_std_4 = np.std(history[-4:]) if len(history) >= 4 else 0.0
            roll_8 = np.mean(history[-8:]) if len(history) >= 8 else lag_1
            roll_max_4 = np.max(history[-4:]) if len(history) >= 4 else lag_1
            roll_min_4 = np.min(history[-4:]) if len(history) >= 4 else lag_1

            row = [
                current_date.month,
                int(current_date.isocalendar().week),
                current_date.quarter,
                current_date.dayofyear,
                len(history),
                lag_1, lag_2, lag_4, lag_8,
                roll_4, roll_std_4, roll_8,
                roll_max_4, roll_min_4
            ]

            feat_array = np.array(row).reshape(1, -1)
            pred = float(max(self.model.predict(feat_array)[0], 0.0))
            forecasts.append(round(pred, 2))
            history.append(pred)  # Recursive feeding

        return forecasts

    def save_model(self, model_dir: str = settings.MODEL_DIR):
        """Persists trained model and metadata."""
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        model_path = Path(model_dir) / "demand_forecaster.joblib"
        meta_path = Path(model_dir) / "forecasting_metadata.json"

        joblib.dump({
            "model": self.model,
            "feature_columns": self.feature_columns,
            "best_model_name": self.best_model_name
        }, model_path)

        with open(meta_path, "w") as f:
            json.dump({
                "best_model_name": self.best_model_name,
                "metrics": self.metrics_summary,
                "feature_columns": self.feature_columns
            }, f, indent=2)

        logger.info(f"Demand forecaster model and metadata saved to {model_dir}")

    def load_model(self, model_dir: str = settings.MODEL_DIR):
        """Loads serialized model artifact."""
        model_path = Path(model_dir) / "demand_forecaster.joblib"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        bundle = joblib.load(model_path)
        self.model = bundle["model"]
        self.feature_columns = bundle["feature_columns"]
        self.best_model_name = bundle.get("best_model_name", "XGBoost_Regressor")
        logger.info(f"Loaded demand forecasting model from {model_path}")
