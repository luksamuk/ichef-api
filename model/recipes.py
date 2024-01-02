from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from datetime import datetime, time, timedelta
import uuid

from db.base import DatabaseModel

class Recipe(DatabaseModel):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    chef_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    text_search = Column(TSVECTOR, nullable=False, index=True)

    chef = relationship('User', back_populates='recipes')

    
