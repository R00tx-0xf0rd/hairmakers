import os
import pathlib

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(__file__),
            "..",
            ".env",
        ),
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_prefix="DB_",
    )
    TYPE: str = None
    NAME: str = None
    HOST: str = None
    PORT: str = None
    USER: str = None
    PASSWORD: str = None
    INIT: bool = False
    echo: bool
    log_level: str = "INFO"
    log_format: str = (
        "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{line} | {message}"
    )

    def get_db_url(self):
        if self.TYPE == "sqlite":
            # data_dir = os.path.join(os.path.(__file__).parent, "data" )
            data_dir = pathlib.Path(__file__).parent.parent / "data/db"
            if not data_dir.exists():
                pathlib.Path(data_dir).mkdir(parents=True)
            db_path = (data_dir / self.NAME).as_posix()
            return f"{self.TYPE}+aiosqlite:///{db_path}"

        return f"{self.TYPE}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


settings = Settings(echo=True)

logger.add("data/logs/log.log", format=settings.log_format, level=settings.log_level)
