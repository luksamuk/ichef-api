from pydantic import BaseModel
from datetime import datetime
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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
