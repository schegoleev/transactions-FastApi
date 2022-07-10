from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

POSTGRES_NAME = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = 1234


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()