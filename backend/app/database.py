"""
NEXUS Database Engine and Session Management
Configured for PostgreSQL production deployment with automatic SQLite local fallback.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import settings
from backend.app.utils.logger import logger

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables in the database."""
    from backend.app.models import orm_models  # noqa
    Base.metadata.create_all(bind=engine)
    logger.info(f"Database initialized with URL: {settings.DATABASE_URL.split('@')[-1]}")
