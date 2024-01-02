from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from schemas import auth as schema
from util import encryption, auth

from repository import users as users_repository

def login(db: Session, payload: schema.Login) -> schema.TokenResponse:
    user = users_repository.get_user_by_email(db, payload.email)
    if user is None:
        raise HTTPException(status_code=401, detail='Cannot login: User does not exist')

    if not encryption.verify_password_hash(user.pw_hash, payload.password):
        raise HTTPException(status_code=401, detail='Cannot login: Incorrect password')

    return auth.jwt_sign(user)

