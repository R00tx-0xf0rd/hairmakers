import asyncio

from sqlalchemy import text

from config.settings import logger, settings
from db import database
from db.dao import ServiceDAO
from db.models import Base, Service


async def main():
    logger.info(settings.get_db_url())
    async with database.async_session() as session:
        try:
            # ← Добавь это: создание таблиц (если их нет)
            async with database.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            srv_dict = {
                "name": "hairstyle",
                "description": "Прическа",
                "duration_minutes": 120,
                "is_active": True,
            }
            service = Service(**srv_dict)

            res = await ServiceDAO(session).add_one(service)
            print(res)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await session.close()
            await database.close()


if __name__ == "__main__":
    asyncio.run(main())
