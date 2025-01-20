from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os
from bot.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
)

async_session = async_sessionmaker(engine)




