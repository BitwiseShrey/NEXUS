"""
Unit Tests for NEXUS Demand Forecasting Models
"""

import numpy as np
import pandas as pd
from ml.forecasting.baseline_models import NaiveForecaster, MovingAverageForecaster
from ml.forecasting.xgboost_forecaster import DemandForecaster
from ml.evaluation.metrics import ModelEvaluator


def test_naive_forecaster():
    y = np.array([10.0, 15.0, 20.0, 25.0])
    model = NaiveForecaster()
    model.fit(y)
    preds = model.predict(horizon=3)
    assert len(preds) == 3
    assert np.all(preds == 25.0)


def test_moving_average_forecaster():
    y = np.array([10.0, 20.0, 30.0, 40.0])
    model = MovingAverageForecaster(window=2)
    model.fit(y)
    preds = model.predict(horizon=2)
    assert len(preds) == 2
    assert preds[0] == 35.0  # mean(30, 40)


def test_regression_metrics():
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 310.0])
    metrics = ModelEvaluator.evaluate_regression(y_true, y_pred)
    assert metrics["MAE"] == 10.0
    assert metrics["RMSE"] == 10.0
    assert metrics["sMAPE_percent"] > 0


def test_demand_forecaster_training():
    dates = pd.date_range("2021-01-01", periods=60, freq="W")
    # Series with trend and seasonal pattern
    demands = [1000 + (i * 20) + (100 * np.sin(i / 4.0)) for i in range(60)]
    df = pd.DataFrame({"date": dates, "demand": demands})

    forecaster = DemandForecaster(random_seed=42)
    results = forecaster.train_and_benchmark(df, "demand", "date")

    assert "winner_model" in results
    assert "evaluation_metrics" in results
    assert "XGBoost_Regressor" in results["evaluation_metrics"]

    # Test future forecast
    future = forecaster.forecast_future(df.tail(12), horizon_steps=4)
    assert len(future) == 4
    assert all(f > 0 for f in future)
