import asyncio
from config.settings import logger, settings
from db import database
from utils import init_db


async def main():
    logger.info(settings.get_db_url())
    try:
        if settings.INIT:
            await init_db()
        else:
            await database.connect()
            await database.execute("SELECT 1")
    except Exception as e:
        logger.error(f"Не удалось подключиться к базе данных: {e}")
    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())
