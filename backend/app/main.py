"""
NEXUS FastAPI Main Application
AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization Platform
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.config import settings
from backend.app.database import init_db
from backend.app.utils.logger import logger
from backend.app.api import (
    health_router,
    entities_router,
    analytics_router,
    forecast_router,
    risk_router,
    anomaly_router,
    impact_router,
    simulation_router,
    optimization_router,
    recommendations_router
)

app = FastAPI(
    title="NEXUS Decision Intelligence Platform API",
    description=(
        "Production-grade backend for AI-powered supply-chain monitoring, demand forecasting, "
        "supervised supplier risk prediction, graph-based impact propagation, scenario simulation, "
        "Google OR-Tools multi-echelon optimization, and actionable recommendation generation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware (configured for local dev and future frontend clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred in NEXUS processing pipeline.", "error": str(exc)}
    )

# Include Routers
app.include_router(health_router)
app.include_router(entities_router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX)
app.include_router(forecast_router, prefix=settings.API_V1_PREFIX)
app.include_router(risk_router, prefix=settings.API_V1_PREFIX)
app.include_router(anomaly_router, prefix=settings.API_V1_PREFIX)
app.include_router(impact_router, prefix=settings.API_V1_PREFIX)
app.include_router(simulation_router, prefix=settings.API_V1_PREFIX)
app.include_router(optimization_router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
def on_startup():
    logger.info("Initializing NEXUS database and services...")
    init_db()
    logger.info("NEXUS backend initialized and ready to receive requests.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
