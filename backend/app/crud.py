from sqlalchemy.orm import Session
from . import models, schemas

def add_items(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_items_batch(db: Session, items_batch: schemas.ItemCreateBatch):
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
        # for item in item_dict:
        #     print(f"Item: {item}, type = {type(item_dict[item])}")
        db_items.append(models.Item(**item_dict))
    
    db.add_all(db_items)
    db.commit()
    for db_item in db_items:
        db.refresh(db_item)
    return db_items