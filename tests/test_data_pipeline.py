"""
Unit and Integration Tests for NEXUS Data Pipeline & Digital Twin Topology
"""

import pandas as pd
import numpy as np
from pipeline.data_preprocessing import DataPreprocessor
from pipeline.feature_engineering import FeatureEngineer
from digital_twin.network_builder import NetworkBuilder
from digital_twin.geo_engine import GeoEngine, INDIAN_HUBS


def test_network_builder_entity_targets(sample_network):
    """Verify digital twin network entities meet all target scales."""
    assert len(sample_network["suppliers"]) == 20
    assert len(sample_network["production_units"]) == 8
    assert len(sample_network["products"]) == 50
    assert len(sample_network["warehouses"]) == 10
    assert len(sample_network["hubs"]) == 15
    assert len(sample_network["demand_zones"]) == 30
    assert len(sample_network["routes"]) >= 100


def test_indian_geocoordinates_validity(sample_network):
    """Verify all entities fall within authentic Indian geographic coordinate bounds."""
    # India bounding box approx: Lat 8 to 36 N, Lon 68 to 97 E
    for s in sample_network["suppliers"]:
        assert 8.0 <= s["latitude"] <= 36.0
        assert 68.0 <= s["longitude"] <= 97.0

    for w in sample_network["warehouses"]:
        assert 8.0 <= w["latitude"] <= 36.0
        assert 68.0 <= w["longitude"] <= 97.0


def test_haversine_and_highway_distance():
    """Verify geospatial calculations between Delhi and Mumbai."""
    delhi = INDIAN_HUBS["DELHI_NCR"]
    mumbai = INDIAN_HUBS["MUMBAI_BHIWANDI"]

    haversine = GeoEngine.haversine_distance(delhi["lat"], delhi["lon"], mumbai["lat"], mumbai["lon"])
    highway = GeoEngine.highway_distance(delhi["lat"], delhi["lon"], mumbai["lat"], mumbai["lon"])

    assert 1100 <= haversine <= 1250  # ~1150 km great circle
    assert highway > haversine        # Highway tortuosity factor


def test_feature_engineering_lags():
    """Verify time-series lag and rolling statistics generation without lookahead leakage."""
    dates = pd.date_range("2022-01-01", periods=20, freq="W")
    demands = [100.0 + i * 5 for i in range(20)]
    df_raw = pd.DataFrame({"date": dates, "demand": demands})

    df_feats = FeatureEngineer.create_forecasting_features(df_raw, "demand", "date")
    assert "lag_1" in df_feats.columns
    assert "lag_4" in df_feats.columns
    assert "rolling_mean_4" in df_feats.columns
    # Check that lag_1 matches previous row's demand
    assert df_feats["lag_1"].iloc[1] == df_feats["demand"].iloc[0]
