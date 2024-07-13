from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database connection parameters
conn_params = {
    "host": "localhost",
    "dbname": "eafc_analysis",
    "user": "postgres",
    "password": "Imp117qang"
}

def get_db():
    db = SessionLocal()  # Create a new Session
    try:
        yield db
    finally:
        db.close()