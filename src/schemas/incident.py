from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class IncidentStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSource(str, Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    SYSTEM = "system"


class IncidentBase(BaseModel):
    description: str = Field(...,
                             min_length=1,
                             description="Описание инцидента")
    source: IncidentSource = IncidentSource.SYSTEM


class IncidentCreate(IncidentBase):
    status: IncidentStatus = IncidentStatus.NEW


class IncidentUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[IncidentStatus] = None
    source: Optional[IncidentSource] = None


class IncidentRead(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime

    class Config:
        from_attributes = True
