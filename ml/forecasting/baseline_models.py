"""
NEXUS Baseline Demand Forecasting Models
Implements benchmark models (Naive, Moving Average) to establish lower performance bounds.
"""

from typing import Dict, Any, List
import numpy as np
from ml.evaluation.metrics import ModelEvaluator


class NaiveForecaster:
    """
    Naive persistence forecast: y_hat(t+h) = y(t).
    Standard baseline in time-series benchmarks.
    """

    def __init__(self):
        self.last_value = 0.0

    def fit(self, y: np.ndarray):
        y_arr = np.asarray(y, dtype=float)
        self.last_value = float(y_arr[-1]) if len(y_arr) > 0 else 0.0
        return self

    def predict(self, horizon: int = 1) -> np.ndarray:
        return np.full(horizon, self.last_value)


class MovingAverageForecaster:
    """
    Moving Average forecast: y_hat(t+h) = mean(y[t-window : t]).
    """

    def __init__(self, window: int = 4):
        self.window = window
        self.mean_value = 0.0

    def fit(self, y: np.ndarray):
        y_arr = np.asarray(y, dtype=float)
        if len(y_arr) >= self.window:
            self.mean_value = float(np.mean(y_arr[-self.window:]))
        elif len(y_arr) > 0:
            self.mean_value = float(np.mean(y_arr))
        else:
            self.mean_value = 0.0
        return self

    def predict(self, horizon: int = 1) -> np.ndarray:
        return np.full(horizon, self.mean_value)
