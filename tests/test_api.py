"""
Integration Tests for NEXUS FastAPI Endpoints
"""

import pytest


def test_api_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ONLINE"
    assert data["database"] == "HEALTHY"
    assert data["all_systems_operational"] is True


def test_api_entities(client):
    # Suppliers
    resp = client.get("/api/v1/suppliers")
    assert resp.status_code == 200
    assert len(resp.json()) == 20

    # Products
    resp = client.get("/api/v1/products")
    assert resp.status_code == 200
    assert len(resp.json()) == 50

    # Warehouses
    resp = client.get("/api/v1/warehouses")
    assert resp.status_code == 200
    assert len(resp.json()) == 10

    # Routes
    resp = client.get("/api/v1/routes")
    assert resp.status_code == 200
    assert len(resp.json()) >= 100

    # Inventory
    resp = client.get("/api/v1/inventory?limit=50")
    assert resp.status_code == 200
    assert len(resp.json()) == 50

    # Demand
    resp = client.get("/api/v1/demand")
    assert resp.status_code == 200
    assert len(resp.json()) == 30

    # Network
    resp = client.get("/api/v1/network")
    assert resp.status_code == 200
    assert resp.json()["total_nodes"] == 83


def test_api_analytics_and_gis(client):
    resp = client.get("/api/v1/analytics/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "suppliers" in data
    assert "inventory" in data
    assert "routes" in data

    resp_gis = client.get("/api/v1/analytics/gis/facilities")
    assert resp_gis.status_code == 200
    gis_data = resp_gis.json()
    assert gis_data["type"] == "FeatureCollection"
    assert gis_data["total_features"] > 0


def test_api_forecast(client):
    payload = {"product_id": "PROD_ITEM_001", "horizon_weeks": 4}
    resp = client.post("/api/v1/forecast", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["forecasted_demand"]) == 4
    assert data["model_name"] == "XGBoost_Regressor"


def test_api_risk_prediction(client):
    payload = {
        "on_time_rate": 0.84,
        "average_delay": 4.2,
        "delay_frequency": 0.16,
        "quality_score": 0.90,
        "lead_time": 5.5,
        "lead_time_variability": 2.0,
        "capacity_utilization": 0.94,
        "historical_delays": 10
    }
    resp = client.post("/api/v1/risk/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "disruption_probability" in data
    assert "risk_drivers" in data


def test_api_unified_risks(client):
    resp = client.get("/api/v1/risks")
    assert resp.status_code == 200
    data = resp.json()
    assert "composite_network_risk_score" in data
    assert "dimensions" in data


def test_api_anomaly_detect(client):
    payload = {
        "events": [
            {"order_id": "EVT_1", "quantity": 25.0, "is_late": 0, "lead_time_deviation": 0.0},
            {"order_id": "EVT_SPIKE", "quantity": 450.0, "is_late": 1, "lead_time_deviation": 10.0}
        ]
    }
    resp = client.post("/api/v1/anomaly/detect", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_events_scanned"] == 2


def test_api_impact_analysis(client):
    payload = {
        "entity_type": "SUPPLIER",
        "entity_id": "SUP_001",
        "capacity_reduction": 0.80,
        "duration_days": 10
    }
    resp = client.post("/api/v1/impact/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["estimated_shortage_units"] > 0
    assert "affected_warehouses_count" in data


def test_api_scenario_simulate(client):
    payload = {
        "scenario_type": "SUPPLIER_FAILURE",
        "parameters": {"supplier_id": "SUP_001", "capacity_reduction": 0.80, "duration_days": 10}
    }
    resp = client.post("/api/v1/scenario/simulate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["applied_disruptions"]) == 1


def test_api_optimization(client):
    payload = {
        "scenario_type": "SUPPLIER_FAILURE",
        "parameters": {"supplier_id": "SUP_001", "capacity_reduction": 0.80, "duration_days": 10},
        "risk_aversion_weight": 50.0
    }
    resp = client.post("/api/v1/optimize", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["nexus_optimized"]["status"] == "OPTIMAL"
    assert "recommendation" in data
    assert "impact_comparison" in data
