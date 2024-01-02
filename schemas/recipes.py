from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class RecipeCommon(BaseModel):
    title: str
    text: str

class RecipeCreate(RecipeCommon):
    # chef_id is deduced from auth data
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

class Recipe(RecipeCommon):
    id: UUID
    chef_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RecipeSearchFilters(BaseModel):
    chef_id: Optional[UUID] = None
    text: Optional[str] = None
