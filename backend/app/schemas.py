from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: str
    is_tradeable: bool
    is_duplicate: bool


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True