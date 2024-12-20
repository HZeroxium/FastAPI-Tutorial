# services/post.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.post import Post as PostModel
from app.schemas.post import PostCreate, PostUpdate
from app.services.auth import TokenData
from fastapi import HTTPException, status


# CRUD functions
def get_all_posts(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(PostModel)
    if search:
        query = query.filter(PostModel.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    return query.all(), query.count()


def get_post_by_id(db: Session, post_id: int):
    return db.query(PostModel).filter(PostModel.id == post_id).first()


def create_post(db: Session, post: PostCreate, current_user: TokenData):
    try:
        db_post = PostModel(**post.model_dump())
        db_post.user_id = current_user.id
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Failed to create post: {str(e)}")


def update_post(
    db: Session, post_id: int, post_update: PostUpdate, current_user: TokenData
):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        return None

    # Ensure the current user owns the post
    if db_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )
    for key, value in post_update.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


def remove_post(db: Session, post_id: int, current_user: TokenData):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        return None
    # Ensure the current user owns the post
    if db_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )
    db.delete(db_post)
    db.commit()
    return db_post
