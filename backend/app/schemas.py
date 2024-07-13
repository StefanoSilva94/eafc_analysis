from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class ItemBase(BaseModel):
    name: str
    pack_name: str
    rating: str
    position: str
    is_tradeable: bool
    is_duplicate: bool

    # Outfield player attributes
    pace: Optional[str] = None
    shooting: Optional[str] = None
    dribbling: Optional[str] = None
    passing: Optional[str] = None
    defending: Optional[str] = None
    physical: Optional[str] = None
    
    # Goalkeeper attributes
    diving: Optional[str] = None
    handling: Optional[str] = None
    kicking: Optional[str] = None
    speed: Optional[str] = None
    reflexes: Optional[str] = None
    positioning: Optional[str] = None


class ItemCreate(ItemBase):
    pass



class ItemRead(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True