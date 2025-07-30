from sqlalchemy.ext.asyncio import create_async_engine

from utils.settings import Settings

SQLALCHEMY_DATABASE_URL = Settings.DB_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
