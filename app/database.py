from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.user}:{settings.password}@{settings.host}/{settings.dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)