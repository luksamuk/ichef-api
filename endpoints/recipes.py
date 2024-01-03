from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from auth.bearers import JWTBearer
import db.connection as db
import repository.recipes as repository
import controllers.recipes as controller
import schemas.recipes as schema
from uuid import UUID

router = APIRouter(
    prefix='/recipes',
    tags=["Recipes"],
    dependencies=[Depends(JWTBearer())],
)

@router.get('/', response_model=list[schema.Recipe])
async def get_recipes(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.get_recipes(db, offset=size * page, limit=size)


@router.get('/{recipe_uuid}', response_model=schema.Recipe)
async def find_recipe_by_id(recipe_uuid: UUID, db: Session = Depends(db.make_session)):
    return controller.get_recipe(db, id=recipe_uuid)


@router.post('/', response_model=schema.Recipe)
async def create_recipe(token: Annotated[str, Depends(JWTBearer())],
                        payload: schema.RecipeCreate,
                        db: Session = Depends(db.make_session)):
    return controller.create_recipe(db, token, payload)


@router.post('/search', response_model=list[schema.Recipe])
async def search_recipe(payload: schema.RecipeSearchFilters, page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.find_recipe(db, payload, offset=size * page, limit=size)


@router.put('/{recipe_uuid}', response_model=schema.Recipe)
async def update_recipe(token: Annotated[str, Depends(JWTBearer())],
                        recipe_uuid: UUID, payload: schema.RecipeUpdate,
                        db: Session = Depends(db.make_session)):
    return controller.update_recipe(db, token, recipe_uuid, payload)


