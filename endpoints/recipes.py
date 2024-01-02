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
async def get_recipes(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return repository.get_recipes(db, offset=size * page, limit=size)


@router.get('/{recipe_uuid}', response_model=schema.Recipe)
async def find_recipe_by_id(recipe_uuid: UUID, db: Session = Depends(db.make_session)):
    entity = repository.get_recipe(db, id=recipe_uuid)
    if entity is None:
        raise HTTPException(status_code=404, detail='Recipe not found')
    return entity


@router.post('/', response_model=schema.Recipe)
async def create_recipe(payload: schema.RecipeCreate, db: Session = Depends(db.make_session)):
    return repository.create_recipe(db, payload)


@router.post('/search', response_model=list[schema.Recipe])
async def search_recipe(payload: schema.RecipeSearchFilters, db: Session = Depends(db.make_session)):
    if (payload.chef_id is None) and (payload.text is None):
        raise HTTPException(status_code=400, detail='Must use at least one filter')

    if payload.text and (len(payload.text) < 3):
        raise HTTPException(status_code=400, detail='Text search must contain at least three characters')
    
    return repository.find_by_filter(db, payload)


@router.put('/{recipe_uuid}', response_model=schema.Recipe)
async def update_recipe(recipe_uuid: UUID, payload: schema.RecipeUpdate, db: Session = Depends(db.make_session)):
    return repository.update_recipe(db, recipe_uuid, payload)


