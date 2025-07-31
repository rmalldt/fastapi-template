from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = Field(default="")
    db_port: str = Field(default="5432")
    db_name: str = Field(default="")
    db_user: str = Field(default="")
    db_password: str = Field(default="")
    secret_key: str = Field(default="")
    algorithm: str = Field(default="")
    access_token_expire_minutes: int = Field(default=1)

    # `.env` is resolved relative to CWD when the uvicorn script is run and
    # the Settings() is instantiated
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
