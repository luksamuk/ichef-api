from sqlalchemy.orm import Session
import uuid

from model import users as model
from schemas import users as schema

def get_user(db: Session, id: uuid.UUID) -> model.User | None:
    return db.query(model.User).filter(model.User.id ==  id).first()

def get_user_by_email(db: Session, email: str) -> model.User | None:
    return db.query(model.User).filter(model.User.email ==  email).first()

def get_users(db: Session, offset: int = 0, limit: int = 100) -> list[model.User]:
    db.query(model.User).offset(offset).limit(limit).all()

# def create_user(db: Session, payload: schema.UserCreate):
    
