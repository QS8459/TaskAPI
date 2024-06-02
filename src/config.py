from pydantic_settings import BaseSettings;
from pydantic import PostgresDsn;

class Settings(BaseSettings):
    app_version: str;
    app_title: str;
    pg_uri: PostgresDsn;
    secret_key:str;
    algorithm: str;
    class Config:
        env_file = ".env";
        env_file_encoding = 'utf-8'

settings = Settings();