from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


oauth2scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "586b8aee8c28c3784c222e70a1b9b0f59cb5774d6d03aaff1f225758337d41ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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