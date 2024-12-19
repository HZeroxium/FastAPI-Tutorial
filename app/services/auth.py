# services/auth.py

from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as UserModel
from app.services.user import get_user_by_email, get_password_hash, verify_password
import jwt
from datetime import datetime, timedelta
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_user(db: Session, user: UserCreate):
    # Check if user already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise ValueError("User already exists")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "access_token": create_access_token({"sub": db_user.email}),
        "token_type": "bearer",
    }
