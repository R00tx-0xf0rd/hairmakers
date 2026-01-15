import json

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import database
from db.dao import MasterDAO, ServiceDAO


class MasterView(BaseModel):
    name: str
    is_active: bool


class ServiceView(BaseModel):
    name: str
    description: str
    duration_minutes: int
    is_active: bool


async def add_masters_to_db(session: AsyncSession):
    with open(settings.MASTERS_JSON, "r", encoding="utf-8") as file:
        tables_data = json.load(file)
    await MasterDAO(session).add_many([MasterView(**table) for table in tables_data])


async def add_services_to_db(session: AsyncSession):
    with open(settings.SERVICES_JSON, "r", encoding="utf-8") as file:
        tables_data = json.load(file)
    await ServiceDAO(session).add_many([ServiceView(**table) for table in tables_data])


async def init_db():
    try:
        async with database.async_session() as session:
            await add_masters_to_db(session)
            await add_services_to_db(session)
            await session.commit()
    except Exception as e:
        raise e
