import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

if DB_URL:
    engine = create_engine(DB_URL)
else:
    raise Exception({"message": "Database URL missing."})

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


# Dependency: Get connection to DB and create DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
