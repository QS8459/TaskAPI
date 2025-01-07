from pydantic_settings import BaseSettings;
from pydantic import PostgresDsn, SecretStr, Extra
class Settings(BaseSettings):
    app_version: str;
    app_title: str;
    app_description: str;
    pg_uri: PostgresDsn;
    # token_expiration: int;
    # secret_key: SecretStr;
    # algorithm: str;
    # smtp_server: str;
    # smtp_port: int;
    # smtp_email: SecretStr;
    # smtp_pass: SecretStr;

    class Config:
        env_file = None,
        env_file_encoding = "utf-8"
        extra = Extra.allow
        env_prefix ="TK_"

settings = Settings();