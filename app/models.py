from sqlalchemy import Boolean, Column, Identity, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

# ----- DBUser


class DBUser(Base):
    __tablename__ = "user_account"
    id = Column(Integer, Identity(always=True), primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# ----- DBPost


class DBPost(Base):
    __tablename__ = "post"

    id = Column(Integer, Identity(always=True), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
