from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db.connection as db
import controllers.auth as controller
import schemas.auth as schema

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"],
)

@router.post('/token', response_model=schema.TokenResponse)
async def login(payload: schema.Login, db: Session = Depends(db.make_session)):
    return controller.login(db, payload)

