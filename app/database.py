import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import settings


DB_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
Base = declarative_base()
if DB_URL:
    engine = create_engine(DB_URL)
else:
    raise Exception({"message": "Database URL missing."})

SessionLocal = sessionmaker(autoflush=False, bind=engine)


# Create DB session for every request to the specific API endpoints and autoclose once done.
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
SessionDep = Annotated[Session, Depends(get_session)]
