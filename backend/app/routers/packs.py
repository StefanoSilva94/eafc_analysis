from .. import crud, models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..database import get_db, engine
from typing import Union, List



router = APIRouter(
    prefix="/packs",
    tags=['Packs']
)


@router.post("/", response_model=List[schemas.ItemRead])
def add_items_batch(items_batch: schemas.ItemCreateBatch, db: Session = Depends(get_db)):
    try:
        db_items = crud.add_items_batch(db=db, items_batch=items_batch)
        return db_items
    except Exception as e:
        print(f"Error adding items: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding the items.")
    
