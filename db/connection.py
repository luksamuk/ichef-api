from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings

def make_connection_string() -> str:
    settings = get_settings()
    return 'postgresql://%s:%s@%s:%s/%s' % (
        settings.database_user,
        settings.database_password,
        settings.database_host,
        settings.database_port,
        settings.database_name
    )

def make_engine(echo=False):
    return create_engine(make_connection_string(), echo=echo)

engine = make_engine(echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def make_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

