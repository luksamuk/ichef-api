from pydantic import BaseModel
from typing import Optional
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

class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_admin: Optional[bool] = None
    old_password: Optional[str] = None
    password: Optional[str] = None

class User(UserCommon):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
