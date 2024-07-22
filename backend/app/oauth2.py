from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .config import settings

oauth2scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user.id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except InvalidTokenError:
        raise credentials_exception
    
    return token_data 


def get_current_user(token: str = Depends(oauth2scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Autheticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)


def verify_login_status(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")

        if exp is None:
            raise credentials_exception
        else:
            current_time = datetime.now(tz=timezone.utc)
            exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)
    
    except InvalidTokenError:
        raise credentials_exception
    
    return current_time < exp_time
