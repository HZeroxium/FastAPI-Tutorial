# schemas/vote.py

from pydantic import BaseModel
from datetime import datetime


class VoteBase(BaseModel):
    post_id: int


class VoteCreate(VoteBase):
    pass


class VoteResponse(BaseModel):
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
