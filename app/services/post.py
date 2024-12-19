# services/post.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.post import Post as PostModel
from app.schemas.post import PostCreate, PostUpdate


# CRUD functions
def get_all_posts(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(PostModel).offset(skip).limit(limit)
    return query.all(), query.count()


def get_post_by_id(db: Session, post_id: int):
    return db.query(PostModel).filter(PostModel.id == post_id).first()


def create_post(db: Session, post: PostCreate):
    try:
        db_post = PostModel(**post.model_dump())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Failed to create post: {str(e)}")


def update_post(db: Session, post_id: int, post_update: PostUpdate):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        return None
    for key, value in post_update.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


def remove_post(db: Session, post_id: int):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
    return db_post
