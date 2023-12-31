from pydantic import BaseModel
from uuid import UUID

class RecipeCommon(BaseModel):
    chef_id: UUID
    title: str
    text: str

class RecipeCreate(RecipeCommon):
    pass

class Recipe(RecipeCommon):
    id: UUID

    class Config:
        orm_mode = True

