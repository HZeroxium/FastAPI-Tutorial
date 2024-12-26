# schemas/user.py

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": {
                "email": "user@example.com",
            }
        }
    }


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": {
                "password": "password123",
                "confirm_password": "password123",
            }
        }
    }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
