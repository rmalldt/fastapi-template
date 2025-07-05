from datetime import datetime
from sqlalchemy import Boolean, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

"""
The recommended SQLAlchemy approach:
    - Mapped[type] tells the type checker that this field is a mapped ORM column stroing the specified type.
    - mapped_colum(...) is the preferred API in SQLAlchemy 2.0+ to declare mapped columns. 

This will:
    - Eliminate type-checking warnings.
    - Ensure our model is compatible with both SQLAlchemcy and static type checkers.
"""


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True, nullable=False
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[str] = mapped_column(
        Boolean, nullable=False, server_default="True"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["UserAccount"] = relationship()


class Vote(Base):
    __tablename__ = "vote"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    )
