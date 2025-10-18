from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, declarative_base
# Load from .env file
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()