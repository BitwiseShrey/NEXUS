"""
NEXUS Structured Logging System
Provides clean, informative logging for data pipelines, ML workflows, optimization runs, and API requests.
"""

import logging
import sys
from backend.app.config import settings

def setup_logger(name: str = "nexus") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger("nexus")
