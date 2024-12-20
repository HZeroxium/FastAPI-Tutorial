# services/user.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils import password
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = password.get_password_hash(user.password)
        db_user = UserModel(
            email=user.email, hashed_password=hashed_password, role="user"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error: {str(e)}")


def get_user(db: Session, include_deleted=False, **kwargs):
    query = db.query(UserModel).filter_by(**kwargs)
    if not include_deleted:
        query = query.filter_by(is_deleted=False)
    return query.first()


def get_user_by_email(db: Session, email: str):
    return get_user(db, email=email)


def get_user_by_id(db: Session, user_id: int):
    return get_user(db, id=user_id)


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id, UserModel.is_deleted == False)
        .first()
    )
    if not db_user:
        return None
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = password.get_password_hash(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id, UserModel.is_deleted == False)
        .first()
    )
    if not db_user:
        return None
    db_user.is_deleted = True  # Soft-delete
    db.commit()
    return db_user
