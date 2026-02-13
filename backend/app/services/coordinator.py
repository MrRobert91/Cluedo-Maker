from sqlmodel import Session, select
from app.models.all_models import Event, EventStatus, Character, Faction, Item, Puzzle, Objective, Participant
from app.services.agents.world_builder import WorldBuilderAgent
from app.core.logging_config import get_logger
import asyncio

logger = get_logger("app.services.coordinator")

async def start_generation_task(event_id: int, session: Session):
    # Re-fetch session/event securely inside the async task if needed, 
    # but for simplicity passing session (careful with async/threading in SQLite)
    # Better to create new session here.
    
    from app.db.session import engine
    with Session(engine) as db:
        event = db.get(Event, event_id)
        if not event:
            return
            
        try:
            event.status = EventStatus.GENERATING
            db.add(event)
            db.commit()
            
            # 1. World Building
            logger.info(f"Starting World Building for {event.name}")
            wb = WorldBuilderAgent()
            world_data = await wb.generate(event.theme, event.tone)
            event.intro_narrative = world_data.get("intro", "")
            
            # Save Factions
            factions_map = {} # name -> id
            for f_data in world_data.get("factions", []):
                faction = Faction(
                    event_id=event_id,
                    name=f_data["name"],
                    description=f_data["description"],
                    objectives=f_data["objectives"]
                )
                db.add(faction)
                db.commit()
                db.refresh(faction)
                factions_map[faction.name] = faction.id

            # 2. Assign Roles & Generate Characters
            participants = db.exec(select(Participant).where(Participant.event_id == event_id)).all()
            
            # Simple Round-Robin or Agentic Assignment
            import random
            roles_definitions = world_data.get("roles", []) # Expecting generic roles if any, or generate on fly
            
            for idx, p in enumerate(participants):
                # Placeholder logic -> Real logic should be Agentic
                char = Character(
                    event_id=event_id,
                    participant_id=p.id,
                    name=f"Agent {p.name}", 
                    bio_public="A mysterious figure.",
                    bio_secret="You are actually a double agent.",
                    is_spy=(idx == 0) # Simple rule: first is spy
                )
                db.add(char)
            
            db.commit()
            
            # 3. Generate Items (Placeholder)
            item = Item(event_id=event_id, name="Revolver", description="A rusty revolver", rule_type="attack", rules="Hits for 1 point.")
            db.add(item)
            
            event.status = EventStatus.READY
            db.add(event)
            db.commit()
            logger.info("Generation Complete")
        except Exception as e:
            logger.error(f"Error generating event {event_id}: {e}", exc_info=True)
            event.status = EventStatus.ERROR
            db.add(event)
            db.commit()
