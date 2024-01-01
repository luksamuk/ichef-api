from fastapi import FastAPI
from db import DatabaseModel, engine

DatabaseModel.metadata.create_all(bind=engine)

