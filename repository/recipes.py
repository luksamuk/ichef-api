from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid

from model import recipes as model
from schemas import recipes as schema

def get_recipe(db: Session, id: uuid.UUID) -> model.Recipe | None:
    return db.query(model.Recipe).filter(model.Recipe.id == id).first()

def get_recipes(db: Session, offset: int = 0, limit: int = 100) -> list[model.Recipe]:
    return db.query(model.Recipe)\
        .order_by(model.Recipe.created_at.asc())\
        .offset(offset).limit(limit)\
        .all()

# TODO: Get number of pages

def create_recipe(db: Session, payload: schema.RecipeCreate) -> model.Recipe:
    # TODO: Check if chef really exists!
    db_model = model.Recipe(
        title = payload.title,
        chef_id = payload.chef_id,
        text = payload.text,
        text_search = func.to_tsvector('portuguese', payload.title + ' ' + payload.text)
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

# TODO: Update recipe


def find_by_filter(db: Session, payload: schema.RecipeFilter, offset: int = 0, limit: int = 100) -> list[model.Recipe]:
    query = db.query(model.Recipe)

    if not (payload.chef_id is None):
        query = query.filter(model.Recipe.chef_id ==  payload.chef_id)

    if not (payload.text is None):
        query = query.filter(
            model.Recipe.text_search\
            .bool_op('@@')(
                func.plainto_tsquery('portuguese', payload.text)
            ))

    return query.offset(offset).limit(limit).all()
