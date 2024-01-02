from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from model import users as model
from schemas import users as schema
from util import encryption


def get_user(db: Session, id: uuid.UUID) -> model.User | None:
    return db.query(model.User).filter(model.User.id ==  id).first()

def get_user_by_email(db: Session, email: str) -> model.User | None:
    return db.query(model.User).filter(model.User.email ==  email).first()

def get_users(db: Session, offset: int, limit: int) -> list[model.User]:
    return db.query(model.User)\
      .order_by(model.User.created_at.asc())\
      .offset(offset).limit(limit)\
      .all()

# TODO: Get number of pages

def get_chefs(db: Session, offset: int, limit: int) -> list[model.User]:
    return db.query(model.User)\
      .order_by(model.User.created_at.asc())\
      .filter(model.User.is_chef)\
      .offset(offset).limit(limit)\
      .all()

def create_user(db: Session, model: model.User) -> model.User:
    db.add(model)
    db.commit()
    db.refresh(db_model)
    return db_model
    
def update_user(db: Session, id: uuid.UUID, payload: schema.UserUpdate) -> model.User:
    db_model = get_user(db, id)
    
    if payload.password is not None:
        db_model.pw_hash = encryption.gen_password_hash(payload.password)

    if payload.name is not None:
        db_model.name = payload.name

    if payload.is_admin is not None:
        db_model.is_admin = payload.is_admin

    db.commit()
    db.refresh(db_model)
    return db_model
