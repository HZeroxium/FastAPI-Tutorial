# config.py
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 10))
DATABASE_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 20))
