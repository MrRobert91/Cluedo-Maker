from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import create_db_and_tables
from app.api.routers import events
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
import os
import time

setup_logging()
logger = get_logger("app.main")

app = FastAPI(title=settings.PROJECT_NAME)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.4f}s"
    )
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routers import events, projects

# API Routers
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

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
