# services/user.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = UserModel(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error: {str(e)}")


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(UserModel)
        .filter(UserModel.id == user_id, UserModel.is_deleted == False)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return (
        db.query(UserModel)
        .filter(UserModel.email == email, UserModel.is_deleted == False)
        .first()
    )


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
        db_user.hashed_password = get_password_hash(user_update.password)
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
