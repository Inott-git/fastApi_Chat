from sqlalchemy.orm import Session
from app import config as cfg
from app.db import schems, models


def get_password_hash(password):
    return cfg.pwd_context.hash(password)


def create_user(session: Session, user: schems.UserDB):
    db_user = models.User(username=user.username, email=user.email, password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return cfg.pwd_context.verify(plain_password, hashed_password)


def get_user(session: Session, email: str):
    user = session.query(models.User).filter(models.User.email == email).first()
    return user


def get_user_id(session: Session, id: int):
    user = session.query(models.User).filter(models.User.id == id).first()
    if not user:
        return {'id':-1,
                'username': '',
                'email': ''}
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = get_user(session, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
