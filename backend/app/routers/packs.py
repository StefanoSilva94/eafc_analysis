from .. import crud, models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..database import get_db, engine
from typing import Union, List



router = APIRouter()


@router.post("/new_item/", response_model=schemas.ItemRead)
def add_items(item: schemas.ItemCreate, db=Depends(get_db)):
    db_item = crud.add_items(db, item)
    return db_item


@router.post("/new_items/", response_model=List[schemas.ItemRead])
def add_items_batch(items_batch: schemas.ItemCreateBatch, db: Session = Depends(get_db)):
    try:
        db_items = crud.add_items_batch(db=db, items_batch=items_batch)
        return db_items
    except Exception as e:
        print(f"Error adding items: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding the items.")
    
