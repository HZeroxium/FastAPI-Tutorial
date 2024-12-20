# services/vote.py

from sqlalchemy.orm import Session
from app.models.vote import Vote as VoteModel
from app.models.post import Post as PostModel
from app.schemas.vote import VoteCreate
from app.schemas.auth import TokenData
from fastapi import HTTPException, status


def create_vote(db: Session, vote: VoteCreate, current_user: TokenData):
    # Check if the post exists
    post = db.query(PostModel).filter(PostModel.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    # Check if the vote already exists
    existing_vote = (
        db.query(VoteModel)
        .filter(VoteModel.post_id == vote.post_id, VoteModel.user_id == current_user.id)
        .first()
    )
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Vote already exists"
        )
    # Create the vote
    new_vote = VoteModel(user_id=current_user.id, post_id=vote.post_id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote


def delete_vote(db: Session, post_id: int, current_user: TokenData):
    # Find the vote
    vote = (
        db.query(VoteModel)
        .filter(VoteModel.post_id == post_id, VoteModel.user_id == current_user.id)
        .first()
    )
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )
    db.delete(vote)
    db.commit()
    return vote


def get_votes_for_post(db: Session, post_id: int):
    # Fetch all votes for a specific post
    return db.query(VoteModel).filter(VoteModel.post_id == post_id).all()


def get_user_votes(db: Session, user_id: int):
    # Fetch all votes by a specific user
    return db.query(VoteModel).filter(VoteModel.user_id == user_id).all()
