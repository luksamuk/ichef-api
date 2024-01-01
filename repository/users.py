from sqlalchemy.orm import Session
import uuid

from model import users as model
from schemas import users as schema
from util.encryption import gen_password_hash


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
    hashed_password = gen_password_hash(payload.password)
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
    
