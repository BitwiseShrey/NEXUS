"""
NEXUS API Routers Package
"""

from backend.app.api.health import router as health_router
from backend.app.api.entities import router as entities_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.forecast import router as forecast_router
from backend.app.api.risk import router as risk_router
from backend.app.api.anomaly import router as anomaly_router
from backend.app.api.impact import router as impact_router
from backend.app.api.simulation import router as simulation_router
from backend.app.api.optimization import router as optimization_router
from backend.app.api.recommendations import router as recommendations_router

__all__ = [
    "health_router",
    "entities_router",
    "analytics_router",
    "forecast_router",
    "risk_router",
    "anomaly_router",
    "impact_router",
    "simulation_router",
    "optimization_router",
    "recommendations_router"
]
