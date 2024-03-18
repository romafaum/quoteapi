from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dbname: str
    host: str
    user: str
    password: str
    secret_key: str

    class Config:
        env_files = [".env"]

settings = Settings()
settings.dbname = "quotesapi"
