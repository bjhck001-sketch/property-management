"""初始化数据库"""
import asyncio
from src.database import engine, Base
from src.models import *  # noqa: F401 - Import all models

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized")

if __name__ == '__main__':
    asyncio.run(init_db())
