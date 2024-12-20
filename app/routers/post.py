# routers/post.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse
from app.schemas.auth import TokenData
from app.services.post import (
    get_all_posts,
    get_post_by_id,
    create_post,
    update_post,
    remove_post,
)
from app.db.database import get_db
from app.services.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=PostListResponse, status_code=status.HTTP_200_OK)
async def get_posts(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to retrieve"),
    search: str = Query(None, description="Search query"),
    db: Session = Depends(get_db),
):
    print(f"Skip: {skip}, Limit: {limit}, Search: {search}")
    posts, total = get_all_posts(db, skip=skip, limit=limit, search=search)
    return {"data": posts, "total": total}


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    return create_post(db, post, current_user)


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.patch("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def patch_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    updated_post = update_post(db, post_id, post, current_user)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return updated_post


@router.delete(
    "/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    deleted_post = remove_post(db, post_id, current_user)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return deleted_post
