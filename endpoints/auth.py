from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db.connection as db
import controllers.auth as controller
import schemas.auth as schema
from schemas.general import HTTPErrorModel

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"],
)

@router.post('/token',
             response_model=schema.TokenResponse,
             responses={
                 401: {
                     "model": HTTPErrorModel,
                     "description": "User does not exist or password is incorrect"
                 }
             })
async def login(payload: schema.Login, db: Session = Depends(db.make_session)):
    return controller.login(db, payload)

