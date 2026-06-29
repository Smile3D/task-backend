from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Движок — соединение с базой
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий — как открыть соединение для запроса
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Dependency для FastAPI — даёт сессию в каждый эндпоинт
async def get_db():
    async with async_session() as session:
        yield session