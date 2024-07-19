from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2
from datetime import timedelta

router = APIRouter(tags=['Authentication'])


@router.get('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id}, expires_delta=timedelta(minutes=300))

    return {"access_token": access_token, "token_type": "bearer"}
