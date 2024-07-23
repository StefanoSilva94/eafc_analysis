from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class ItemBase(BaseModel):
    name: str
    user_id: int
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

class PlayerPickBase(ItemBase):
    pass


class PlayerPickCreate(PlayerPickBase):
    is_selected: bool


class PlayerPickCreateBatch(BaseModel):
    items: List[PlayerPickCreate]
    pack_name: str


class ItemCreateBatch(BaseModel):
    items: List[ItemCreate]
    pack_name: str

class ItemRead(ItemBase):
    id: int
    pack_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlayerPickRead(PlayerPickBase):
    id: int
    pack_id: int
    created_at: datetime
    is_selected: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: Optional[int]


class TokenData(BaseModel):
    id: Optional[str]


class TokenStatus(BaseModel):
    is_valid: bool
    error: str = None