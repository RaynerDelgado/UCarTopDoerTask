from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependencies import get_async_session
from src.models.incident import Incident as IncidentModel
from src.schemas.incident import IncidentCreate, IncidentUpdate, IncidentRead


class IncidentManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_incidents(self,
                                status: Optional[str] = None
                                ) -> List[IncidentModel]:
        query = select(IncidentModel)
        if status:
            query = query.where(IncidentModel.status == status)
        result = await self.session.execute(query)
        incidents = result.scalars().all()
        return incidents

    async def get_incident(self, incident_id: int) -> IncidentModel:
        query = select(IncidentModel).where(IncidentModel.id == incident_id)
        result = await self.session.execute(query)
        incident = result.scalars().first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        return incident

    async def create_incident(self,
                              incident_data: IncidentCreate) -> IncidentModel:
        incident = IncidentModel(description=incident_data.description,
                                 status=incident_data.status,
                                 source=incident_data.source)
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def update_incident(
            self, incident_id: int,
            incident_update: IncidentUpdate) -> IncidentModel:
        incident = await self.get_incident(incident_id)

        update_data = incident_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(incident, field, value)

        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def delete_incident(self, incident_id: int) -> IncidentModel:
        incident = await self.get_incident(incident_id)
        await self.session.delete(incident)
        await self.session.commit()
        return incident


async def get_incident_manager(
        session: AsyncSession = Depends(get_async_session)):
    return IncidentManager(session)
