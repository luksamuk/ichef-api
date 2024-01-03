import uvicorn
from fastapi import FastAPI
from endpoints import users, recipes, auth
from config.settings import get_settings
from schemas.general import PingModel

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    summary='API iChef para chefs e cozinheiros',
    description='API REST para compartilhamento de receitas entre chefs e cozinheiros amadores.',
    version='1.0.0',
    contact={
        "name": "Lucas S. Vieira",
        "url": "https://luksamuk.codes/",
        "email": "lucasvieira@protonmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/MIT/",
    },
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recipes.router)


@app.get('/ping', tags=['Healthcheck'], response_model=PingModel)
async def ping():
    return PingModel(message='pong')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
