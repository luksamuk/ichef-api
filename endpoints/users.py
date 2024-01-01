from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db
import repository.users as repository
import schemas.users as schema

router = APIRouter(
    prefix='/users',
    tags=["users"],
)

@router.get('/')
async def get_users(db: Session = Depends(db.make_session)):
    return repository.get_users(db)


@router.post('/', response_model=schema.User)
def create_user(payload: schema.UserCreate, db: Session = Depends(db.make_session)):
    if repository.get_user_by_email(db, email=payload.email):
        raise HTTPException(status_code=409, detail='User already exists')
    return repository.create_user(db, payload)

