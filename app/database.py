from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .setts import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.user}:{settings.password}@{settings.host}/{settings.dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
