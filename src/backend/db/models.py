from datetime import UTC, date, datetime

from sqlalchemy import JSON, Date, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), unique=True, default="owner")
    birth_date: Mapped[date] = mapped_column(Date)
    sex: Mapped[str] = mapped_column(String(8))
    height_cm: Mapped[float] = mapped_column(Float)
    training_years: Mapped[float] = mapped_column(Float, default=0.0)
    activity_level: Mapped[str] = mapped_column(String(16))
    goal: Mapped[str] = mapped_column(String(16))
    equipment: Mapped[list[str]] = mapped_column(JSON, default=list)
    injuries: Mapped[list[str]] = mapped_column(JSON, default=list)
    chronic_conditions: Mapped[list[str]] = mapped_column(JSON, default=list)
    medications: Mapped[list[str]] = mapped_column(JSON, default=list)
    diet_restrictions: Mapped[list[str]] = mapped_column(JSON, default=list)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list)
    red_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow
    )
