from .. import crud, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from ..database import get_db
from typing import List
from .. utils.futbin_utils import update_player_data_with_price


router = APIRouter(
    prefix="/packs",
    tags=['Packs']
)


@router.post("/", response_model=List[schemas.ItemRead])
def add_items_batch(items_batch: schemas.ItemCreateBatch, db: Session = Depends(get_db)):
    try:

        updated_items_batch = update_player_data_with_price(items_batch)
        db_items = crud.add_items_batch(db=db, items_batch=updated_items_batch)
        return db_items
    except Exception as e:
        print(f"Error adding items: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding the items.")
    
