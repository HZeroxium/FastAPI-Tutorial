# config.py
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

DATABASE_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 10))
DATABASE_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 20))

DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_course")
# Database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
)
