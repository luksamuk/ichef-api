from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = 'Teste Técnico Workalove'
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: str
    
    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings() -> Settings:
    return Settings()

