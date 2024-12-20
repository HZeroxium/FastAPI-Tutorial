# services/auth.py

from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.auth import TokenData
from app.models.user import User as UserModel
from app.services.user import get_user_by_email
from app.utils.password import verify_password, get_password_hash
import jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    to_encode["sub"] = str(to_encode["sub"])  # Convert sub to a string
    print(f"Token payload: {to_encode}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    """
    Verify the validity of an access token.
    """
    try:
        print(f"Verifying token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")
        user_id: str = payload.get("sub")
        print(f"User ID from payload: {user_id}")
        if user_id is None:
            print("User ID is None; raising credentials exception.")
            raise credentials_exception
        return TokenData(
            id=user_id, email=payload.get("email"), role=payload.get("role")
        )  # Ensure TokenData is consistent with payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Received token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tokenData = verify_access_token(token, credentials_exception)
    return tokenData


def get_current_admin_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = get_user_by_email(
        db, token_data.id
    )  # Assuming this retrieves the user by email
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.
    """
    # Check if user already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "access_token": create_access_token({"sub": db_user.id}),
        "token_type": "bearer",
    }
