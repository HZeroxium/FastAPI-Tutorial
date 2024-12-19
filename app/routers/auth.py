# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Form, Body, Request
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from app.services.auth import authenticate_user, create_access_token, create_user
from app.db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginForm:
    def __init__(
        self,
        email: str = Body(None),
        password: str = Body(None),
        form_email: str = Form(None),
        form_password: str = Form(None),
    ):
        self.email = email or form_email
        self.password = password or form_password
        if not self.email or not self.password:
            raise HTTPException(
                status_code=422, detail="Both email and password are required fields."
            )


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        token = create_user(db, user)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request, form_data: LoginForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
