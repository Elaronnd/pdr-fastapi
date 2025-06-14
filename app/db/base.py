from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)
from app.config.config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_ADDRESS,
    DB_PORT,
    DB_NAME
)

engine = create_async_engine(f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}',
                             echo=True)


class Base(DeclarativeBase):
    ...


Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
