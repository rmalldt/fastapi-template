from sqlalchemy import Boolean, Column, Identity, Integer, String, null
from database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, Identity(always=True), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="False")
