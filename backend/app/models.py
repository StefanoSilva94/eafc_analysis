from .database import Base
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from pydantic import EmailStr
import datetime


class Item(Base):
    __tablename__ = "packed_items"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=0)
    pack_id = Column(Integer, ForeignKey('packs.id'), nullable=False)  # Foreign key to packs table
    pack_name = Column(String)  
    name = Column(String, index=True)
    rating = Column(String)  
    position = Column(String)  
    is_tradeable = Column(Boolean, server_default='false')
    is_duplicate = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))
    pace = Column(String, nullable=True)  
    shooting = Column(String, nullable=True)  
    dribbling = Column(String, nullable=True)  
    passing = Column(String, nullable=True)  
    defending = Column(String, nullable=True)  
    physical = Column(String, nullable=True)  
    
    # Goalkeeper attributes
    diving = Column(String, nullable=True)
    handling = Column(String, nullable=True)
    kicking = Column(String, nullable=True)
    speed = Column(String, nullable=True)
    reflexes = Column(String, nullable=True)
    positioning = Column(String, nullable=True)

    # Futbin cols
    base_id = Column(String, nullable=True)
    resource_id = Column(String, nullable=True)
    league = Column(String, nullable=True)
    nation = Column(String, nullable=True)
    raretype = Column(String, nullable=True)
    rare = Column(String, nullable=True)
    price = Column(Integer, nullable=True)

    pack = relationship("Pack", back_populates="items")


class Pack(Base):
    __tablename__ = "packs"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    pack_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))
    items = relationship("Item", back_populates="pack")
    picks = relationship("PlayerPick", back_populates="pack")


class PlayerPick(Base):
    __tablename__ = "player_picks"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=0)
    pack_id = Column(Integer, ForeignKey('packs.id'), nullable=False)  # Foreign key to packs table
    pack_name = Column(String)  
    name = Column(String, index=True)
    rating = Column(String)  
    position = Column(String)  
    is_tradeable = Column(Boolean, server_default='false')
    is_duplicate = Column(Boolean)
    is_selected = Column(Boolean, server_default='false')  # New column
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))
    pace = Column(String, nullable=True)  
    shooting = Column(String, nullable=True)  
    dribbling = Column(String, nullable=True)  
    passing = Column(String, nullable=True)  
    defending = Column(String, nullable=True)  
    physical = Column(String, nullable=True)  
    
    # Goalkeeper attributes
    diving = Column(String, nullable=True)
    handling = Column(String, nullable=True)
    kicking = Column(String, nullable=True)
    speed = Column(String, nullable=True)
    reflexes = Column(String, nullable=True)
    positioning = Column(String, nullable=True)

    # Futbin cols
    base_id = Column(String, nullable=True)
    resource_id = Column(String, nullable=True)
    league = Column(String, nullable=True)
    nation = Column(String, nullable=True)
    raretype = Column(String, nullable=True)
    rare = Column(String, nullable=True)
    price = Column(Integer, nullable=True)

    pack = relationship("Pack", back_populates="picks")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))

    # Django-specific fields you are adding:
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    date_joined = Column(TIMESTAMP(timezone=True), server_default=text('now()'))