from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from auth.bearers import JWTBearer
import db.connection as db
import controllers.users as controller
import schemas.users as schema
from uuid import UUID

import repository.users as repository

router = APIRouter(
    prefix='/users',
    tags=["Users"],
)

@router.get('/', response_model=list[schema.User], dependencies=[Depends(JWTBearer())])
async def get_users(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.get_users(db, offset=size * page, limit=size)


@router.get('/chefs', response_model=list[schema.User], dependencies=[Depends(JWTBearer())])
async def get_chefs(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.get_chefs(db, offset=size * page, limit=size)


@router.post('/', response_model=schema.User)
async def create_user(token: Annotated[str, Depends(JWTBearer())],
                      payload: schema.UserCreate,
                      db: Session = Depends(db.make_session)):
    return controller.create_user(db, token, payload)


@router.get('/{user_uuid}', response_model=schema.User, dependencies=[Depends(JWTBearer())])
async def find_user_by_id(user_uuid: UUID, db: Session = Depends(db.make_session)):
    return controller.get_user(db, id=user_uuid)


@router.get('/email/{user_email}', response_model=schema.User, dependencies=[Depends(JWTBearer())])
async def find_user_by_email(user_email: str, db: Session = Depends(db.make_session)):
    return controller.get_user_by_email(db, email=user_email)


@router.put('/{user_uuid}', response_model=schema.User)
async def update_user(token: Annotated[str, Depends(JWTBearer())],
                      user_uuid: UUID, payload: schema.UserUpdate,
                      db: Session = Depends(db.make_session)):
    return controller.update_user(db, token, user_uuid, payload)

