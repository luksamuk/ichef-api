from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, time, timedelta
import uuid

from db.base import DatabaseModel

class User(DatabaseModel):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    pw_hash = Column(String(256), nullable=False)
    is_chef = Column(Boolean, default=False, index=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    recipes = relationship('Recipe', back_populates='chef')
