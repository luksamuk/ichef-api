from pydantic import BaseModel
from typing import Optional
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


class RecipeFilter(BaseModel):
    chef_id: Optional[UUID] = None
    text: Optional[str] = None
