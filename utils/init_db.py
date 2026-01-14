import json

from loguru import logger

from db import database
from db.dao import ServiceDAO


async def init_db():
    with open("data/db/json/services.json", encoding="utf-8") as f:
        services = json.load(f)

    async with database.async_session() as session:
        cnt = await ServiceDAO(session).add_many(services["services"])
        if cnt:
            logger.success(f"Успешно добавлено {cnt} услуг")
