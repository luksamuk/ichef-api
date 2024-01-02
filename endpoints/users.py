from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db.connection as db
import repository.users as repository
import schemas.users as schema
from uuid import UUID

router = APIRouter(
    prefix='/users',
    tags=["Users"],
)

@router.get('/', response_model=list[schema.User])
async def get_users(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return repository.get_users(db, offset=size * page, limit=size)


@router.get('/chefs', response_model=list[schema.User])
async def get_chefs(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return repository.get_chefs(db, offset=size * page, limit=size)


@router.post('/', response_model=schema.User)
async def create_user(payload: schema.UserCreate, db: Session = Depends(db.make_session)):
    if repository.get_user_by_email(db, email=payload.email):
        raise HTTPException(status_code=409, detail='User already exists')
    return repository.create_user(db, payload)


@router.get('/{user_uuid}', response_model=schema.User)
async def find_user_by_id(user_uuid: UUID, db: Session = Depends(db.make_session)):
    entity = repository.get_user(db, id=user_uuid)
    if entity is None:
        raise HTTPException(status_code=404, detail='User not found')
    return entity


@router.get('/email/{user_email}', response_model=schema.User)
async def find_user_by_email(user_email: str, db: Session = Depends(db.make_session)):
    entity = repository.get_user_by_email(db, email=user_email)
    if entity is None:
        raise HTTPException(status_code=404, detail='User not found')
    return entity


@router.put('/{user_uuid}', response_model=schema.User)
async def update_user(user_uuid: UUID, payload: schema.UserUpdate, db: Session = Depends(db.make_session)):
    return repository.update_user(db, user_uuid, payload)
