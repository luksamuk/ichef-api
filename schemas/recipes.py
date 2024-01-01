from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class RecipeCommon(BaseModel):
    chef_id: UUID
    title: str
    text: str

class RecipeCreate(RecipeCommon):
    pass

class Recipe(RecipeCommon):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

