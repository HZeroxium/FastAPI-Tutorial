# routers/vote.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.vote import VoteCreate, VoteResponse
from app.services.vote import (
    create_vote,
    delete_vote,
    get_votes_for_post,
    get_user_votes,
)
from app.services.auth import get_current_user
from app.db.database import get_db
from app.schemas.auth import TokenData

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def add_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    return create_vote(db, vote, current_user)


@router.delete(
    "/{post_id}", response_model=VoteResponse, status_code=status.HTTP_200_OK
)
async def remove_vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    return delete_vote(db, post_id, current_user)


@router.get("/post/{post_id}", response_model=List[VoteResponse])
async def get_votes(post_id: int, db: Session = Depends(get_db)):
    return get_votes_for_post(db, post_id)


@router.get("/user", response_model=List[VoteResponse])
async def get_my_votes(
    db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    return get_user_votes(db, current_user.id)
