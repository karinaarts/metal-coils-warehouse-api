from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, CheckConstraint, DateTime

from src.database import Base


class CoilModel(Base):
    __tablename__ = "coils"

    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[float] = mapped_column(CheckConstraint("length > 0"))
    weight: Mapped[float] = mapped_column(CheckConstraint("weight > 0"))
    creation_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    deletion_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
