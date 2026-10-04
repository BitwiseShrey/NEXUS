"""
NEXUS Machine Learning Evaluation Metrics
Standardized calculations for regression and classification models.
"""

from typing import Dict, Any
import numpy as np
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error,
    precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)


class ModelEvaluator:
    """
    Computes rigorous evaluation metrics for ML and baseline models.
    """

    @staticmethod
    def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculates MAE, RMSE, and MAPE/sMAPE.
        """
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)

        mae = float(mean_absolute_error(y_true, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))

        # Symmetric MAPE to prevent division by zero
        denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
        diff = np.abs(y_pred - y_true)
        # Avoid zero division
        nonzero = denominator != 0
        if np.any(nonzero):
            smape = float(np.mean(diff[nonzero] / denominator[nonzero]) * 100)
        else:
            smape = 0.0

        return {
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "sMAPE_percent": round(smape, 2)
        }

    @staticmethod
    def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> Dict[str, Any]:
        """
        Calculates Precision, Recall, F1, ROC-AUC, and Confusion Matrix.
        """
        y_true = np.asarray(y_true, dtype=int)
        y_pred = np.asarray(y_pred, dtype=int)

        precision = float(precision_score(y_true, y_pred, zero_division=0))
        recall = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))

        roc_auc = 0.5
        if y_prob is not None and len(np.unique(y_true)) > 1:
            try:
                roc_auc = float(roc_auc_score(y_true, y_prob))
            except Exception:
                roc_auc = 0.5

        cm = confusion_matrix(y_true, y_pred).tolist()

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": cm
        }
