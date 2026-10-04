"""
NEXUS Pytest Fixtures and Global Configurations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base, get_db
from backend.app.main import app
from digital_twin.network_builder import NetworkBuilder
from simulation.scenario_engine import SimulationState


@pytest.fixture(scope="session")
def test_db_session():
    """Provides a memory/test SQLite database session for unit tests."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def sample_network():
    """Provides generated digital twin sample entities."""
    builder = NetworkBuilder(seed=42)
    sups = builder.generate_suppliers()
    prods = builder.generate_production_units()
    products = builder.generate_products(sups)
    whs = builder.generate_warehouses()
    hubs = builder.generate_distribution_hubs()
    dzs = builder.generate_demand_zones(products)
    rts = builder.generate_routes(sups, prods, whs, hubs, dzs)
    return {
        "suppliers": sups,
        "production_units": prods,
        "products": products,
        "warehouses": whs,
        "hubs": hubs,
        "demand_zones": dzs,
        "routes": rts
    }
