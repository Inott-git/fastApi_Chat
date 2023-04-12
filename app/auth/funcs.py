from datetime import datetime, timedelta
from typing import Annotated
import app.db as db
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from app import auth
from app.auth.configs import oauth2_scheme
import app.config as cfg


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(db.database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = auth.schems.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.crud.get_user(session=session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user



