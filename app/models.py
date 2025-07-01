from datetime import datetime
import datetime
from sqlalchemy import Boolean, Column, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
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

# ----- DBUser


class DBUser(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# ----- DBPost


class DBPost(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True, nullable=False
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[str] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
