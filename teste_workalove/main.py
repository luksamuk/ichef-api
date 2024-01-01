from fastapi import FastAPI
from endpoints import users, recipes

app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)

@app.get('/')
async def root():
    return {"message": "Hello, world!"}

