import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()
DB_URL = os.getenv("DB_URL")

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
