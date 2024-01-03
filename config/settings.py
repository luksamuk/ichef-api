from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = 'iChef'
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: str
    api_port: int
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiry_seconds: int
    
    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings() -> Settings:
    return Settings()

