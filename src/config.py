from pydantic_settings import BaseSettings;
from pydantic import PostgresDsn, SecretStr
class Settings(BaseSettings):
    app_version: str;
    app_title: str;
    pg_uri: PostgresDsn;
    token_expiration: int;
    secret_key: SecretStr;
    algorithm: str;

    class Config:
        env_file = ".env",
        env_file_encoding = "utf-8"

settings = Settings();