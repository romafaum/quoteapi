from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dbname: str
    host: str
    user: str
    password: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()