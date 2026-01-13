from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.models import Base


class MasterService(Base):
    __tablename__ = "master_services"

    master_id: Mapped[int] = mapped_column(
        ForeignKey("masters.id", ondelete="CASCADE"),
        primary_key=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint("master_id", "service_id", name="uq_master_service"),
    )
