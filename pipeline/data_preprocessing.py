"""
NEXUS Data Preprocessing and Cleaning Module
Handles data normalization, missing values, data validation, and transformation.
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from backend.app.utils.logger import logger


class DataPreprocessor:
    """
    Standardizes and cleans empirical datasets and digital twin records.
    """

    @staticmethod
    def clean_walmart_sales(df: pd.DataFrame) -> pd.DataFrame:
        """Clean Walmart sales historical demand data."""
        logger.info(f"Preprocessing Walmart demand series. Initial records: {len(df)}")
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        # Remove negative sales or return artifacts for baseline demand estimation
        df["Weekly_Sales"] = df["Weekly_Sales"].apply(lambda x: max(float(x), 0.0))
        df["IsHoliday"] = df["IsHoliday"].astype(int)
        df = df.sort_values(by=["Store", "Dept", "Date"]).reset_index(drop=True)
        return df

    @staticmethod
    def clean_dataco_logistics(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize DataCo supply chain delivery data."""
        logger.info(f"Preprocessing DataCo logistics records. Initial records: {len(df)}")
        df = df.copy()

        # Select relevant core columns
        expected_cols = [
            "Days for shipping (real)",
            "Days for shipment (scheduled)",
            "Delivery Status",
            "Late_delivery_risk",
            "Order Item Quantity",
            "Sales"
        ]
        available_cols = [c for c in expected_cols if c in df.columns]
        df = df[available_cols].dropna().copy()

        # Calculate empirical lead-time variance
        if "Days for shipping (real)" in df.columns and "Days for shipment (scheduled)" in df.columns:
            df["delay_days"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
            df["is_delayed"] = (df["delay_days"] > 0).astype(int)

        return df

    @staticmethod
    def validate_entity_counts(entities: Dict[str, list]) -> bool:
        """Validate that digital twin entity counts satisfy project targets."""
        checks = {
            "suppliers": (len(entities.get("suppliers", [])), 20),
            "production_units": (len(entities.get("production_units", [])), 8),
            "products": (len(entities.get("products", [])), 50),
            "warehouses": (len(entities.get("warehouses", [])), 10),
            "distribution_hubs": (len(entities.get("distribution_hubs", [])), 15),
            "demand_zones": (len(entities.get("demand_zones", [])), 30),
            "routes": (len(entities.get("routes", [])), 100),
            "orders": (len(entities.get("orders", [])), 50000),
            "disruptions": (len(entities.get("disruptions", [])), 500),
        }

        all_passed = True
        for name, (count, target) in checks.items():
            if count < target:
                logger.warning(f"Validation warning: {name} count ({count}) is below target ({target})")
                all_passed = False
            else:
                logger.info(f"Validation passed: {name} count = {count} (target >= {target})")

        return all_passed
