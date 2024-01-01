from sqlalchemy import create_engine, Column, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import get_settings

def make_engine():
    settings = get_settings()
    return create_engine(
        'postgresql://%s:%s@%s:%s/%s' % (
            settings.database_user,
            settings.database_password,
            settings.database_host,
            settings.database_port,
            settings.database_name
        ))

engine = make_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DeclarativeBase = declarative_base()

class DatabaseModel(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

def make_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

