from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from model import users as model
from schemas import users as schema
from util import encryption, validation


def get_user(db: Session, id: uuid.UUID) -> model.User | None:
    return db.query(model.User).filter(model.User.id ==  id).first()

def get_user_by_email(db: Session, email: str) -> model.User | None:
    return db.query(model.User).filter(model.User.email ==  email).first()

def get_users(db: Session, offset: int = 0, limit: int = 100) -> list[model.User]:
    return db.query(model.User)\
      .order_by(model.User.created_at.asc())\
      .offset(offset).limit(limit)\
      .all()

# TODO: Get number of pages

def get_chefs(db: Session, offset: int = 0, limit: int = 100) -> list[model.User]:
    return db.query(model.User)\
      .order_by(model.User.created_at.asc())\
      .filter(model.User.is_chef)\
      .offset(offset).limit(limit)\
      .all()

def create_user(db: Session, payload: schema.UserCreate) -> model.User:
    hashed_password = encryption.gen_password_hash(payload.password)
    # TODO: Criar um mapper
    # TODO: Verificar se pode criar o usuário como admin de acordo com a sessão
    db_model = model.User(
        name=payload.name,
        email=payload.email,
        pw_hash=hashed_password,
        is_chef=payload.is_chef,
        is_admin=payload.is_admin
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
    
def update_user(db: Session, id: uuid.UUID, payload: schema.UserUpdate) -> model.User:
    # TODO: This belongs to a controller.
    if (payload.password is None) and\
       (payload.name is None) and\
       (payload.is_admin is None):
        raise HTTPException(status_code=400, detail='Nothing needs to be changed')
    
    # TODO: Verificar se pode criar o usuário como admin de acordo com a sessão
    db_model = get_user(db, id)
    if db_model is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    if payload.password is not None:
        if payload.old_password is None:
            raise HTTPException(status_code=401, detail='Must inform old password to change the password')
        if not encryption.verify_password_hash(db_model.pw_hash, payload.old_password):
            raise HTTPException(status_code=401, detail='Incorrect old password')
        if not validation.is_valid_password(payload.password):
            raise HTTPException(status_code=400, detail='New password is invalid')
        db_model.pw_hash = encryption.gen_password_hash(payload.password)

    if payload.name is not None:
        db_model.name = payload.name

    if payload.is_admin is not None:
        db_model.is_admin = payload.is_admin

    db.commit()
    db.refresh(db_model)
    return db_model
