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
    total_value = 0  # Variable to store total price

    for item in items_batch.items:
        item_dict = item.model_dump()
        item_dict['pack_id'] = pack.id  # Assign the pack ID to each item

        # Depending on the type, create either PlayerPick or Item models
        if type == 'pick':
            db_items.append(models.PlayerPick(**item_dict))
            if item_dict.get('is_selected', False):
                item_price = item_dict.get('price', 0)  # Assuming each item has a 'price' field
                if item_price:
                    total_value += item_price
        else:
            # If there's a price field in item, add it to the total
            item_price = item_dict.get('price', 0)  # Assuming each item has a 'price' field
            if item_price:
                total_value += item_price
            db_items.append(models.Item(**item_dict))

    # Add all items to the database
    db.add_all(db_items)
    db.commit()

    # Refresh items after commit
    for db_item in db_items:
        db.refresh(db_item)

    # Set the total value to the pack's pack_value
    pack.pack_value = total_value
    db.commit()
    db.refresh(pack)

    return db_items
