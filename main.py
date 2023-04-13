from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
import app.db as db
import app.auth as auth
import app.config as cfg


router = FastAPI()


@router.post("/token")
def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.database.get_db)):
    user = db.crud.authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
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

@router.get("/users/me/", response_model=db.schems.User)
async def read_users_me(
    current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]
):
    return current_user

@router.get('/')
async def index(request: Request):
    return cfg.template.TemplateResponse('home.html', context={'request': request})