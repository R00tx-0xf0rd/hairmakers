from sqlalchemy import select

from db.dao import BaseDAO
from db.models import Service


class ServiceDAO(BaseDAO):

    async def list_active(self) -> list[Service]:
        stmt = select(Service).where(Service.is_active.is_(True))
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def get_by_id(self, service_id: int) -> Service | None:
        return await self.session.get(Service, service_id)

    async def add_one(self, service: Service) -> int:
        self.session.add(service)
        res = await self.session.flush()
        await self.session.commit()
        return res
