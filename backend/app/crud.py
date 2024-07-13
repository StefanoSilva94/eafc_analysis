# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def add_items(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
