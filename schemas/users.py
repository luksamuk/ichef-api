from pydantic import BaseModel
from uuid import UUID

from .recipes import Recipe

class UserCommon(BaseModel):
    name: str
    email: str
    is_chef: bool
    is_admin: bool

class UserCreate(UserCommon):
    password: str

class User(UserCommon):
    id: UUID
    recipes: list[Recipe] = [] # TODO: Informação demais na resposta?

    class Config:
        orm_mode = True
