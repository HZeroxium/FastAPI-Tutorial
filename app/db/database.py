# db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import DATABASE_URL, DATABASE_POOL_SIZE, DATABASE_MAX_OVERFLOW


if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Create database connection
engine = create_engine(
    DATABASE_URL,
    pool_size=DATABASE_POOL_SIZE,
    max_overflow=DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Ensures connections are valid before usage
)

# Create a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class
Base = declarative_base()


# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
