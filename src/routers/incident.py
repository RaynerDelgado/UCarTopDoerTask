from typing import List, Optional
from fastapi import Depends, Query
from fastapi.routing import APIRouter

from src.managers.incident import IncidentManager, get_incident_manager
from src.schemas.incident import IncidentCreate, IncidentRead, IncidentUpdate

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("/", response_model=List[IncidentRead])
async def get_incidents(
        status: Optional[str] = Query(None, description="Фильтр по статусу"),
        incidents_manager: IncidentManager = Depends(get_incident_manager)):
    return await incidents_manager.get_all_incidents(status)


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(
    incident_id: int,
    incidents_manager: IncidentManager = Depends(get_incident_manager)):
    return await incidents_manager.get_incident(incident_id)


@router.post("/", response_model=IncidentRead, status_code=201)
async def create_incident(
    incident: IncidentCreate,
    incidents_manager: IncidentManager = Depends(get_incident_manager)):
    return await incidents_manager.create_incident(incident)


@router.patch("/{incident_id}", response_model=IncidentRead)
async def update_incident(
    incident_id: int,
    incident_update: IncidentUpdate,
    incidents_manager: IncidentManager = Depends(get_incident_manager)):
    return await incidents_manager.update_incident(incident_id,
                                                   incident_update)


@router.delete("/{incident_id}", response_model=IncidentRead)
async def delete_incident(
    incident_id: int,
    incidents_manager: IncidentManager = Depends(get_incident_manager)):
    return await incidents_manager.delete_incident(incident_id)
