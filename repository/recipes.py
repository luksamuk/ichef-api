from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
import uuid

from model import recipes as model
from schemas import recipes as schema

def get_recipe(db: Session, id: uuid.UUID) -> model.Recipe | None:
    return db.query(model.Recipe).filter(model.Recipe.id ==  id).first()

def get_recipes(db: Session, offset: int, limit: int) -> list[model.Recipe]:
    return db.query(model.Recipe)\
        .order_by(model.Recipe.created_at.asc())\
        .offset(offset).limit(limit)\
        .all()

# TODO: Get number of pages

def create_recipe(db: Session, model: model.Recipe) -> model.Recipe:
    model.text_search =\
        func.to_tsvector('portuguese', model.title + ' ' + model.text)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def find_by_filter(db: Session, payload: schema.RecipeSearchFilters, offset: int, limit: int) -> list[model.Recipe]:
    query = db.query(model.Recipe)

    if payload.chef_id is not None:
        query = query.filter(model.Recipe.chef_id ==  payload.chef_id)

    if payload.text is not None:
        query = query.filter(
            model.Recipe.text_search\
            .bool_op('@@')(
                func.plainto_tsquery('portuguese', payload.text)
            ))

    return query.offset(offset).limit(limit).all()


def update_recipe(db: Session, id: uuid.UUID, payload: schema.RecipeUpdate) -> model.Recipe:
    db_model = get_recipe(db, id)

    if payload.title is not None:
        db_model.title = payload.title

    if payload.text is not None:
        db_model.text = payload.text

    # If title or text were updated, we need to update the text
    # search index as well
    if (payload.title is not None) or (payload.text is not None):
        db_model.text_search =\
            func.to_tsvector('portuguese', db_model.title + ' ' + db_model.text)

    db.commit()
    db.refresh(db_model)
    return db_model


