from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.services.excel_service import ExcelParsingService
from app.models.all_models import Event, EventStatus, Participant, Faction
from typing import Dict, Any

router = APIRouter()

@router.post("/upload")
async def upload_project_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Uploads an Excel file to create a new Project (Event).
    Parses participants and initializes the project draft.
    """
    # 1. Parse Excel
    participants_data = await ExcelParsingService.parse_participants(file)
    num_participants = len(participants_data)
    
    # 2. Logic to suggest factions based on participants
    # Heuristic: 1 faction per ~3-4 people, min 2 factions.
    suggested_factions = max(2, num_participants // 3)
    
    # 3. Create Event Draft
    new_event = Event(
        name=f"Project {file.filename.split('.')[0]}",
        theme="Classic Mystery", # Default, user will change later
        tone="Suspenseful",      # Default
        num_participants=num_participants,
        status=EventStatus.DRAFT
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    
    # 4. Create Participants
    for p_data in participants_data:
        participant = Participant(
            event_id=new_event.id,
            name=p_data["name"],
            notes=p_data.get("notes")
        )
        session.add(participant)
    
    # 5. Create Default Suggested Factions (Placeholders)
    # User will rename them later in the config wizard
    for i in range(1, suggested_factions + 1):
        faction = Faction(
            event_id=new_event.id,
            name=f"Faction {i}",
            description="To be defined.",
            objectives="To be defined."
        )
        session.add(faction)
        
    session.commit()
    
    return {
        "project_id": new_event.id,
        "project_name": new_event.name,
        "participants_count": num_participants,
        "suggested_factions_count": suggested_factions,
        "message": "Project created successfully from Excel."
    }
