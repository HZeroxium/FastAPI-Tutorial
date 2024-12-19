# routers/post.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse
from app.services.post import (
    get_all_posts,
    get_post_by_id,
    create_post,
    update_post,
    remove_post,
)
from app.db.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=PostListResponse, status_code=status.HTTP_200_OK)
async def get_posts(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to retrieve"),
    db: Session = Depends(get_db),
):
    posts, total = get_all_posts(db, skip=skip, limit=limit)
    return {"data": posts, "total": total}


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.patch("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def patch_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post(db, post_id, post)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return updated_post


@router.delete(
    "/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post = remove_post(db, post_id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return deleted_post
