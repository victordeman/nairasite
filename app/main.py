import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers.api import router as api_router
from app.routers.pages import router as pages_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    try:
        await init_db()
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        # On Vercel, we might want to continue even if init_db fails
        # but let's see if we can get more info
    yield
    logger.info("Shutting down application...")

app = FastAPI(title="NAIRA - African AI & XR Excellence Hub", lifespan=lifespan)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Include routers
app.include_router(api_router)
app.include_router(pages_router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
