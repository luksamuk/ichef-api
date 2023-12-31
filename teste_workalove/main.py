from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
# from model.generic import Message

app = FastAPI()

from db import DatabaseModel, SessionLocal, engine
import repository.users as users

DatabaseModel.metadata.create_all(bind=engine)

def make_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root():
    return {"message": "Hello, world!"}

@app.get('/users')
async def get_users(db: Session = Depends(make_db_session)):
    return users.get_users(db)

# @app.get("/example")
# async def statusmsg() -> Message:
#     return Message(status=200, description="OK")

