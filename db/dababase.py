from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


class DB:
    def __init__(self):
        url = settings.get_db_url()
        echo = settings.echo
        self.engine = create_async_engine(url=url, echo=echo)
        self.async_session = async_sessionmaker(
            self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_maker(self):
        """Возвращает новый асинхронный сеанс."""
        return self.async_session()

    async def close(self):
        if self.engine:
            await self.engine.dispose()
            self.engine = None


database = DB()
