from sqlalchemy import ForeignKey, String, CheckConstraint, Text, Date, Double, DateTime, Index, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass

class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    url: Mapped[str | None] = mapped_column(Text)
    license: Mapped[str | None] = mapped_column(String(30)) 


class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text, server_default="country")
    continent: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(
            "kind IN ('country', 'region', 'world')",
            name="check_valid_kind"
        ),
    )

class Indicator(Base):
    __tablename__ = "indicators"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(Text)
    frequency: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))

    __table_args__ = (
        CheckConstraint(
            "frequency IN ('annual', 'monthly')", 
            name="check_valid_frequency"
        ),
    )

class Observation(Base):
    __tablename__ = "observations"
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), primary_key=True)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("indicators.id"), primary_key=True)
    period: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    value: Mapped[float] = mapped_column(Double)
    loaded_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
    CheckConstraint(
        "EXTRACT(DAY FROM period) = 1",
        name="check_period_first_day",
    ),
    Index("idx_observations_indicator_period", "indicator_id", "period"),
)
