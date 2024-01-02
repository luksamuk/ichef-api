import uvicorn
from fastapi import FastAPI
from endpoints import users, recipes
from config.settings import get_settings

app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)

@app.get('/', tags=['Ping'])
async def ping():
    return { 'message': 'pong' }

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
