from fastapi import FastAPI, Depends, HTTPException
from typing import Union, List
from pydantic import BaseModel
import logging
from .database import get_db, engine
from . import crud, models, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)


conn_params = {
    "host": "localhost",
    "dbname": "eafc_analysis",
    "user": "postgres",
    "password": "Imp117qang"
}
print('hello world')

# Pydantic model for Post request
class Post(BaseModel):
    title: str
    content: str
    publish: bool


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Another example endpoint
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Endpoint to create posts
@app.post("/createposts")
def submit_post(post: Post):
    print(post)
    return {"data": post.title}

# Endpoint to test database connection
@app.get("/sqlalc")
def test_db(db: Session = Depends(get_db)):
    try:
        item = db.query(models.Item).limit(1).first()  # Fetch the first item

        if not item:
                raise HTTPException(status_code=404, detail="Item not found")
        
        return {"player": item}
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/new_item/", response_model=schemas.ItemRead)
def add_items(item: schemas.ItemCreate, db=Depends(get_db)):
    db_item = crud.add_items(db, item)
    return db_item


@app.post("/new_items/", response_model=List[schemas.ItemRead])
def add_items_batch(items_batch: schemas.ItemCreateBatch, db: Session = Depends(get_db)):
    try:
        db_items = crud.add_items_batch(db=db, items_batch=items_batch)
        return db_items
    except Exception as e:
        print(f"Error adding items: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding the items.")
        