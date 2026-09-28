import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .api import complaints, master_tickets, predictive, whatsapp, analytics, agents
from .db.seed_data import seed_database_and_export

from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("civicsense")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing CivicSense AI engine & seeding data...")
    seed_database_and_export()
    logger.info("Initialization complete. Ready for citizen complaints.")
    yield

app = FastAPI(
    title="CivicSense AI - SamAashwas API",
    description="Municipal Grievance Intelligence & Predictive Maintenance Platform for Indian ULBs",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for cross-origin frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api/v1
api_prefix = "/api/v1"
app.include_router(complaints.router, prefix=api_prefix)
app.include_router(master_tickets.router, prefix=api_prefix)
app.include_router(predictive.router, prefix=api_prefix)
app.include_router(whatsapp.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(agents.router, prefix=api_prefix)

@app.get(f"{api_prefix}/health", tags=["System Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount frontend directory for easy standalone viewing and PWA support
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    css_dir = os.path.join(frontend_dir, "css")
    js_dir = os.path.join(frontend_dir, "js")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")

    @app.get("/manifest.json", include_in_schema=False)
    async def serve_manifest():
        return FileResponse(os.path.join(frontend_dir, "manifest.json"), media_type="application/manifest+json")

    @app.get("/sw.js", include_in_schema=False)
    async def serve_sw():
        return FileResponse(os.path.join(frontend_dir, "sw.js"), media_type="application/javascript")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_file = os.path.join(frontend_dir, "index.html")
        return FileResponse(index_file)
