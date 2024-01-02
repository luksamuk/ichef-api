from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

DeclarativeBase = declarative_base()

class DatabaseModel(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

