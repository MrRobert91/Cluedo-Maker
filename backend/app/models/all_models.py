from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class EventStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    READY = "ready"
    ERROR = "error"

class Faction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    name: str
    description: str
    objectives: str
    
    event: "Event" = Relationship(back_populates="factions")
    characters: List["Character"] = Relationship(back_populates="faction")

class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    participant_id: Optional[int] = Field(foreign_key="participant.id")
    faction_id: Optional[int] = Field(foreign_key="faction.id", nullable=True)
    
    name: str = Field(default="Unknown")
    bio_public: str = Field(default="")
    bio_secret: str = Field(default="")
    role_play_tips: str = Field(default="")
    is_spy: bool = Field(default=False)
    image_url: Optional[str] = Field(default=None)
    
    event: "Event" = Relationship(back_populates="characters")
    participant: Optional["Participant"] = Relationship(back_populates="character")
    faction: Optional[Faction] = Relationship(back_populates="characters")
    objectives: List["Objective"] = Relationship(back_populates="character")
    items: List["Item"] = Relationship(back_populates="character")

class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    name: str
    original_photo_url: Optional[str] = Field(default=None)
    
    event: "Event" = Relationship(back_populates="participants")
    character: Optional[Character] = Relationship(back_populates="participant")

class Objective(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="character.id")
    description: str
    type: str = Field(default="individual") # individual, faction
    is_secret: bool = Field(default=True)
    points: int = Field(default=10)
    
    character: Character = Relationship(back_populates="objectives")

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    owner_character_id: Optional[int] = Field(foreign_key="character.id", nullable=True)
    name: str
    description: str
    rule_type: str # attack, defense, utility
    rules: str
    image_url: Optional[str] = Field(default=None)
    
    event: "Event" = Relationship(back_populates="items")
    character: Optional[Character] = Relationship(back_populates="items")

class Puzzle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    title: str
    description: str
    solution: str
    location_hint: str
    
    event: "Event" = Relationship(back_populates="puzzles")

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    theme: str
    tone: str = Field(default="mystery")
    num_participants: int = Field(default=0)
    status: EventStatus = Field(default=EventStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    intro_narrative: str = Field(default="")
    
    participants: List[Participant] = Relationship(back_populates="event")
    characters: List[Character] = Relationship(back_populates="event")
    factions: List[Faction] = Relationship(back_populates="event")
    items: List[Item] = Relationship(back_populates="event")
    puzzles: List[Puzzle] = Relationship(back_populates="event")
