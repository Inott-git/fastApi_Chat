from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response
from app import db
from app import auth
from app import config as cfg
router = APIRouter()


@router.post("/token", response_model=auth.schems.Token)
def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.database.get_db)):
    user = db.crud.authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.funcs.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)  #set HttpOnly cookie in response
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
async def logout(respounse: Response):
    respounse.delete_cookie(key='access_token')
    return 'Secsessful logout'

@router.post('/reg', response_model=db.schems.User)
async def register_user(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], session: Session = Depends(db.database.get_db)):
    new_user = db.crud.create_user(user=db.schems.UserDB(username=username, email=email, password=password), session=session)
    return new_user