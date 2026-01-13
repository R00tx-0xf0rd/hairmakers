import asyncio

from sqlalchemy import text

from config.settings import logger, settings
from db import database
from db.models import Base


async def main():
    logger.info(settings.get_db_url())
    async with database.async_session() as session:
        try:
            # ← Добавь это: создание таблиц (если их нет)
            async with database.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            result = await session.execute(
                text(
                    "insert into services (name, description, duration_minutes, is_active) values ('man_haircut', 'Стрижка мужская', 20, 'true')"
                )
            )
            await session.commit()
            logger.success("Tables created, DB file should now exist.")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await session.close()
            await database.close()


if __name__ == "__main__":
    asyncio.run(main())
