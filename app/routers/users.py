from ..utils import auth_utils
from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from ..database import get_db
from sqlalchemy import text


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = auth_utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
        

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user


@router.post("/get-user-id/")
def get_user_id(email: str, db: Session = Depends(get_db)):
    # Use a raw SQL query to search for the user by email
    result = db.execute(text("SELECT id FROM auth_user WHERE username = :email"), {"email": email}).fetchone()

    # If a user is found, return the user ID, else return 0
    if result:
        return {"user_id": result[0]}
    return {"user_id": 0}