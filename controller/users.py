from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import users as repository
from model import users as model
from schemas import users as schema
from util import encryption, validation


def get_user(db: Session, id: uuid.UUID) -> model.User:
    entity = repository.get_user(db, id)
    if entity is None:
        raise HTTPException(status_code=404, detail='User not found')
    return entity


def get_user_by_email(db: Session, email: str) -> model.User:
    entity = repository.get_user_by_email(db, email)
    if entity is None:
        raise HTTPException(status_code=404, detail='User not found')
    return entity


def get_users(db: Session, offset: int = 0, limit: int = 100) -> list[model.User]:
    return repository.get_users(db, offset, limit)


def get_chefs(db: Session, offset: int = 0, limit: int = 100) -> list[model.User]:
    return repository.get_chefs(db, offset, limit)


def create_user(db: Session, payload: schema.UserCreate) -> model.User:
    if repository.get_user_by_email(db, email=payload.email):
        raise HTTPException(status_code=409, detail='User already exists')
    
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
    return repository.create_user(db, model=db_model)


def update_user(db: Session, id: uuid.UUID, payload: schema.UserUpdate) -> model.User:
    if (payload.password is None) and\
       (payload.name is None) and\
       (payload.is_admin is None):
        raise HTTPException(status_code=400, detail='Nothing needs to be changed')

    if repository.get_user(db, id) is None:
        raise HTTPException(status_code=404, detail='User not found')

    if payload.password is not None:
        if payload.old_password is None:
            raise HTTPException(status_code=401, detail='Must inform old password to change the password')
        if not encryption.verify_password_hash(db_model.pw_hash, payload.old_password):
            raise HTTPException(status_code=401, detail='Incorrect old password')
        if not validation.is_valid_password(payload.password):
            raise HTTPException(status_code=400, detail='New password is invalid')

    return repository.update_user(db, id, payload)

