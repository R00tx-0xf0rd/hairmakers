from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db.dao import BaseDAO
from db.models import Service


class ServiceDAO(BaseDAO):
    model = Service

    async def list_active(self) -> list[Service]:
        stmt = select(self.model).where(Service.is_active.is_(True))
        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def add_one(self, service: Service):
        self._session.add(service)
        await self._session.flush()
        await self._session.commit()
        return service.id

    async def add_many(self, services: list[dict[Any, Any]]):
        models = [Service(**service) for service in services]
        try:
            self._session.add_all(models)
            await self._session.commit()
        except SQLAlchemyError as e:
            logger.error("Невозможно добавить услуги: {}", e)
        return len(models)
