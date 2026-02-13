from pydantic import BaseModel
from typing import List, Optional
from app.models.all_models import EventStatus

class EventCreate(BaseModel):
    name: str
    theme: str
    tone: str = "mystery"

class ParticipantCreate(BaseModel):
    name: str

class EventRead(BaseModel):
    id: int
    name: str
    theme: str
    tone: str
    status: EventStatus
    num_participants: int
