from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import create_db_and_tables
from app.api.routers import events
from app.core.config import settings
import os

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(events.router, prefix="/api/events", tags=["events"])

# Mount static files (uploaded photos, generated pdfs/images)
if not os.path.exists(settings.STATIC_DIR):
    os.makedirs(settings.STATIC_DIR)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "ok"}
