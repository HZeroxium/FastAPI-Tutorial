# models/post.py

from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())

    # Foreign key linking to User.id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to user
    owner = relationship("User", back_populates="posts")

    # Relationship to votes
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_posts_title", "title"),)  # Index for title column
