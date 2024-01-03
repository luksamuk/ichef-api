from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from util.auth import jwt_decode
from schemas.auth import JWTPayload
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


def create_user(db: Session, token: str | None, payload: schema.UserCreate, is_admin: bool) -> model.User:
    if token is not None:
        # An administrator can only be created by another administrator
        auth_data: JWTPayload = jwt_decode(token)
        if is_admin and (not auth_data.is_admin):
            raise HTTPException(
                status_code=403,
                detail='Only an administrator can create another administrator'
            )
    
    if repository.get_user_by_email(db, email=payload.email):
        raise HTTPException(status_code=409, detail='User already exists')
    
    hashed_password = encryption.gen_password_hash(payload.password)
    db_model = model.User(
        name=payload.name,
        email=payload.email,
        pw_hash=hashed_password,
        is_chef=payload.is_chef,
        is_admin=is_admin,
    )
    return repository.create_user(db, model=db_model)


def update_user(db: Session, token: str, id: uuid.UUID, payload: schema.UserUpdate) -> model.User:
    auth_data: JWTPayload = jwt_decode(token)
    
    if (payload.password is None) and\
       (payload.name is None) and\
       (payload.is_admin is None):
        raise HTTPException(status_code=400, detail='Nothing needs to be changed')

    # To update an user, you must either be an admin or the referred user
    if (not auth_data.is_admin) or (str(id) != auth_data.user_id):
        raise HTTPException(
            status_code=403,
            detail='A user can only be changed by an administrator or by themself'
        )
    
    db_model = repository.get_user(db, id)
    if db_model is None:
        raise HTTPException(status_code=404, detail='User not found')

    if payload.password is not None:
        if payload.old_password is None:
            raise HTTPException(status_code=401, detail='Must inform old password to change the password')
        if not encryption.verify_password_hash(db_model.pw_hash, payload.old_password):
            raise HTTPException(status_code=401, detail='Incorrect old password')
        if not validation.is_valid_password(payload.password):
            raise HTTPException(status_code=400, detail='New password is invalid')

    return repository.update_user(db, id, payload)

