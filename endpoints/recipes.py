from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import db
import repository.recipes as repository
import schemas.recipes as schema
from uuid import UUID

router = APIRouter(
    prefix='/recipes',
    tags=["Recipes"],
)

@router.get('/', response_model=list[schema.Recipe])
async def get_recipes(page: int = 0, page_size: int = 100, db: Session = Depends(db.make_session)):
    return repository.get_recipes(db, offset=page_size * page, limit=page_size)

@router.post('/', response_model=schema.Recipe)
def create_recipe(payload: schema.RecipeCreate, db: Session = Depends(db.make_session)):
    return repository.create_recipe(db, payload)

