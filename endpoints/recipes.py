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

@router.post('/search', response_model=list[schema.Recipe])
def find_recipe(payload: schema.RecipeFilter, db: Session = Depends(db.make_session)):
    if (payload.chef_id is None) and (payload.text is None):
        raise HTTPException(status_code=400, detail='Must use at least one filter')

    if payload.text and (len(payload.text) < 3):
        raise HTTPException(status_code=400, detail='Text search must contain at least three characters')

    return repository.find_by_filter(db, payload)
