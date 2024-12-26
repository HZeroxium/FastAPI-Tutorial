# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import user, post, vote
from app.db.database import Base, get_db
from app.config import TEST_DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set!")

# Create test database engine
engine = create_engine(TEST_DATABASE_URL)

# Create a session for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def reset_database():
    """Reset the database schema and clean up any residual state."""
    with engine.connect() as connection:
        logger.info("Terminating all connections to the database...")
        connection.execute(
            text(
                """
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = current_database()
                AND pid <> pg_backend_pid();
                """
            )
        )
        logger.info("Dropping and recreating the schema...")
        connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))
        connection.commit()

    # Clear SQLAlchemy's metadata cache to prevent stale objects
    Base.metadata.clear()

    # Ensure all models are imported before creating tables
    from app.models import user, post  # Import all models explicitly

    logger.info("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")


# Database setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure the database is clean before and after the test session."""
    logger.info("Setting up test database...")
    reset_database()
    yield
    logger.info("Tearing down test database...")
    reset_database()


# Dependency override for database session
@pytest.fixture()
def override_get_db():
    """Override the `get_db` dependency with a test session."""

    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db


# FastAPI test client
@pytest.fixture()
def client(override_get_db):
    """Provide a test client with the overridden dependency."""
    return TestClient(app)
