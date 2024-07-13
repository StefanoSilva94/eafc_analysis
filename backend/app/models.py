from .database import Base
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker


class Item(Base):
    __tablename__ = "packed_items"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)  
    is_tradeable = Column(Boolean, server_default='FALSE')
    is_duplicate = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))


# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:Imp117qang@localhost/eafc_analysis"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# Create the database tables
# Base.metadata.create_all(bind=engine)
