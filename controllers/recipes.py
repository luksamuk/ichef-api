from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from util.auth import jwt_decode
from schemas.auth import JWTPayload
from model import recipes as model
from schemas import recipes as schema
from repository import recipes as repository
from repository import users as users_repository

def get_recipe(db: Session, id: uuid.UUID) -> model.Recipe:
    entity = repository.get_recipe(db, id)
    if entity is None:
        raise HTTPException(status_code=404, detail='Recipe not found')
    return entity


def get_recipes(db: Session, offset: int = 0, limit: int = 100) -> list[model.Recipe]:
    return repository.get_recipes(db, offset, limit)


def create_recipe(db: Session, token: str, payload: schema.RecipeCreate) -> model.Recipe:
    auth_data: JWTPayload = jwt_decode(token)
    
    if users_repository.get_user(db, id=auth_data.user_id) is None:
        raise HTTPException(status_code=500, detail='Could not find current user data')
    
    if not auth_data.is_chef:
        raise HTTPException(status_code=400, detail='Current user is not a chef')
    
    db_model = model.Recipe(
        title = payload.title,
        chef_id = uuid.UUID(auth_data.user_id),
        text = payload.text,
    )
    return repository.create_recipe(db, model=db_model)


def find_recipe(db: Session, payload: schema.RecipeSearchFilters, offset: int = 0, limit: int = 100) -> list[model.Recipe]:
    if (payload.chef_id is None) and (payload.text is None):
        raise HTTPException(status_code=400, detail='No search filters provided')

    if (payload.text is not None) and (len(payload.text) < 3):
        raise HTTPException(status_code=400, detail='Text search must contain at least three characters')
    
    return repository.find_by_filter(db, payload, offset, limit)


def update_recipe(db: Session, token: str, id: uuid.UUID, payload: schema.RecipeUpdate) -> model.Recipe:
    auth_data: JWTPayload = jwt_decode(token)
    
    if (payload.title is None) and (payload.text is None):
        raise HTTPException(status_code=400, detail='Nothing needs to be changed')

    db_model = repository.get_recipe(db, id)
    if db_model is None:
        raise HTTPException(status_code=404, detail='Recipe not found')

    # To update a recipe, you must either be an admin or own it.
    # We also do not enforce the chef role; if, for some reason, this property
    # is changed, the user should still be able to change the recipe.
    if (not auth_data.is_admin) and (str(db_model.chef_id) != auth_data.user_id):
        raise HTTPException(
            status_code=403,
            detail='A recipe can only be changed by an administrator or by its owner'
        )

    return repository.update_recipe(db, id, payload)

