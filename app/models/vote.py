# models/vote.py

from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("user_id", "post_id"),)

    # Relationships
    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")
