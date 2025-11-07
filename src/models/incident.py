from sqlalchemy import Enum as AlchemyEnum, DateTime
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.models.base import Base
from src.schemas.incident import IncidentStatus, IncidentSource


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    description: Mapped[str] = mapped_column(String,
                                             index=True,
                                             nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        AlchemyEnum(IncidentStatus,
                    values_callable=lambda x: [e.value for e in x]),
        default=IncidentStatus.NEW.value,
        nullable=False)
    source: Mapped[IncidentSource] = mapped_column(
        AlchemyEnum(IncidentSource,
                    values_callable=lambda x: [e.value for e in x]),
        default=IncidentSource.SYSTEM,
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.utcnow,
                                                 nullable=False)
