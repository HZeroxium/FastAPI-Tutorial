# schemas/post.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from .user import UserResponse


class PostBase(BaseModel):
    title: str = Field(..., max_length=100, example="My Post Title")
    content: str = Field(..., min_length=10, max_length=500, example="Post content.")
    published: Optional[bool] = Field(
        default=False, description="Whether the post is published."
    )
    rating: Optional[int] = Field(None, ge=0, le=5, example=3)

    @field_validator("title", "content", mode="before")
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner: UserResponse
    votes: int

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    data: List[PostResponse]
    total: int
