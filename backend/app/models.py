from .database import Base
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "packed_items"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
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

    pack = relationship("Pack", back_populates="picks")
