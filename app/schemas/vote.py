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

    model_config = {"from_attributes": True}
