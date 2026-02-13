from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Annotated
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.all_models import Event, Participant, Character, Item
from app.schemas.base import EventCreate, EventRead, ParticipantCreate
from app.core.config import settings
from app.services.coordinator import start_generation_task
import shutil
import os
import uuid

router = APIRouter()

@router.post("/", response_model=EventRead)
def create_event(event: EventCreate, session: Session = Depends(get_session)):
    db_event = Event.model_validate(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/{event_id}/participants")
def add_participants(event_id: int, participants: List[ParticipantCreate], session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for p in participants:
        db_p = Participant(event_id=event_id, name=p.name)
        session.add(db_p)
    
    event.num_participants = len(participants) + len(event.participants)
    session.add(event)
    session.commit()
    return {"status": "ok", "count": len(participants)}

@router.post("/{event_id}/upload-photo")
async def upload_photo(
    event_id: int, 
    participant_name: str = Form(...), 
    file: UploadFile = File(...)
):
    # Determine extension
    ext = file.filename.split(".")[-1]
    filename = f"{event_id}_{uuid.uuid4()}.{ext}"
    file_path = os.path.join(settings.STATIC_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"url": f"/static/{filename}", "participant_name": participant_name}

@router.post("/{event_id}/generate")
async def generate_cluedo(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Trigger background task (using simple async for now, could be Celery)
    # in a real app, use BackgroundTasks
    await start_generation_task(event_id, session)
    
    return {"status": "generation_started"}
