from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..utils import auth_utils
from ..database import get_db
from .. import models, oauth2, schemas
from datetime import timedelta

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not auth_utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    user_id = user.id
    access_token = oauth2.create_access_token(data = {"user_id": user.id}, expires_delta=timedelta(minutes=300))

    return {"access_token": access_token, "token_type": "bearer", "user_id": user_id}


@router.post("/login/verify-token", response_model=schemas.TokenStatus)
def verify_token_expiry(token: schemas.Token):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = token.access_token
    try:
        is_valid = oauth2.verify_login_status(token_data, credentials_exception)
        return schemas.TokenStatus(is_valid=is_valid)
    except HTTPException as e:
        return schemas.TokenStatus(is_valid=False, error=str(e.detail))
    


