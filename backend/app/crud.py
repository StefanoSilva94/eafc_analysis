from sqlalchemy.orm import Session
from . import models, schemas
from typing import Union

def add_items(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_items_batch(db: Session, items_batch: Union[schemas.ItemCreateBatch, schemas.PlayerPickCreateBatch], type='pack'):
    # Create a new pack
    pack = models.Pack(pack_name=items_batch.pack_name)
    db.add(pack)
    db.commit()
    db.refresh(pack)
    
    # Create items with the generated pack_id
    db_items = []
    for item in items_batch.items:

        item_dict = item.model_dump()
        item_dict['pack_id'] = pack.id  # Assign the pack ID to each item

        if type == 'pick':
            db_items.append(models.PlayerPick(**item_dict))
        else:
            db_items.append(models.Item(**item_dict))

    db.add_all(db_items)
    db.commit()
    for db_item in db_items:
        db.refresh(db_item)
    return db_items