from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db
import repository.users as repository
import schemas.users as schema
from uuid import UUID

router = APIRouter(
    prefix='/recipes',
    tags=["Recipes"],
)
