from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from auth.bearers import JWTBearer
import db.connection as db
import repository.recipes as repository
import controllers.recipes as controller
import schemas.recipes as schema
from schemas.general import HTTPErrorModel
from uuid import UUID

router = APIRouter(
    prefix='/recipes',
    tags=["Recipes"],
    dependencies=[Depends(JWTBearer())],
)

@router.get('/', response_model=list[schema.Recipe])
async def get_recipes(page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.get_recipes(db, offset=size * page, limit=size)


@router.get('/{recipe_uuid}',
            response_model=schema.Recipe,
            responses={
                404: {
                    "model": HTTPErrorModel,
                    "description": "Recipe not found",
                }
            })
async def find_recipe_by_id(recipe_uuid: UUID, db: Session = Depends(db.make_session)):
    return controller.get_recipe(db, id=recipe_uuid)


@router.post('/',
             response_model=schema.Recipe,
             responses={
                 400: {
                     "model": HTTPErrorModel,
                     "description": "Current user is not a chef",
                 },
                 500: {
                     "model": HTTPErrorModel,
                     "description": "Current user does not exist",
                 }
             })
async def create_recipe(token: Annotated[str, Depends(JWTBearer())],
                        payload: schema.RecipeCreate,
                        db: Session = Depends(db.make_session)):
    return controller.create_recipe(db, token, payload)


@router.post('/search',
             response_model=list[schema.Recipe],
             responses={
                 400: {
                     "model": HTTPErrorModel,
                     "description": "No search filters provided or text search has less than three characters",
                 }
             })
async def search_recipe(payload: schema.RecipeSearchFilters, page: int = 0, size: int = 100, db: Session = Depends(db.make_session)):
    return controller.find_recipe(db, payload, offset=size * page, limit=size)


@router.put('/{recipe_uuid}',
            response_model=schema.Recipe,
            responses={
                400: {
                    "model": HTTPErrorModel,
                    "description": "No changeable fields were provided",
                },
                403: {
                    "model": HTTPErrorModel,
                    "description": "Session user does not own recipe nor is an administrator",
                },
                404: {
                    "model": HTTPErrorModel,
                    "description": "Recipe not found",
                },
            })
async def update_recipe(token: Annotated[str, Depends(JWTBearer())],
                        recipe_uuid: UUID,
                        payload: schema.RecipeUpdate,
                        db: Session = Depends(db.make_session)):
    return controller.update_recipe(db, token, recipe_uuid, payload)


@router.delete('/{recipe_uuid}',
               status_code=204,
               responses={
                   403: {
                       "model": HTTPErrorModel,
                       "description": "Session user does not own recipe nor is an administrator",
                   }
               })
async def delete_recipe(token: Annotated[str, Depends(JWTBearer())],
                        recipe_uuid: UUID,
                        db: Session = Depends(db.make_session)):
    controller.delete_recipe(db, token, id=recipe_uuid)
