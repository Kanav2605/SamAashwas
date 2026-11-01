import os
import json
import logging
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .api import complaints, master_tickets, predictive, whatsapp, analytics, agents, cities, auth, dispatch, contractors, stream
from .db.seed_data import seed_database_and_export
from .db.database import db
from .core.realtime import realtime_hub
from fastapi import HTTPException

from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("civicsense")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing CivicSense AI engine & seeding data...")
    seed_database_and_export()
    # Start real-time background telemetry loop
    telemetry_task = asyncio.create_task(realtime_hub.telemetry_background_loop())
    logger.info("Initialization complete. Real-time engine & WebSocket stream active.")
    try:
        yield
    finally:
        realtime_hub.is_telemetry_running = False
        telemetry_task.cancel()
        logger.info("Real-time telemetry stream shut down cleanly.")

app = FastAPI(
    title="CivicSense AI - SamAashwas API",
    description="Municipal Grievance Intelligence & Predictive Maintenance Platform for Indian ULBs",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS with strict origin validation (S4 compliance)
cors_origins_list = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
if "*" in cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register API Routers under /api/v1
api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(cities.router, prefix=api_prefix)
app.include_router(complaints.router, prefix=api_prefix)
app.include_router(master_tickets.router, prefix=api_prefix)
app.include_router(predictive.router, prefix=api_prefix)
app.include_router(whatsapp.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(agents.router, prefix=api_prefix)
app.include_router(dispatch.router, prefix=api_prefix)
app.include_router(contractors.router, prefix=api_prefix)
app.include_router(stream.router, prefix=api_prefix)

@app.websocket("/ws/live")
@app.websocket("/ws")
async def root_websocket_endpoint(websocket: WebSocket):
    """
    Direct WebSocket connection on root /ws and /ws/live for instantaneous real-time streaming.
    """
    await realtime_hub.register_websocket(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            try:
                msg = json.loads(text)
                if msg.get("action") == "PING":
                    await websocket.send_text(json.dumps({
                        "type": "PONG",
                        "client_timestamp": msg.get("timestamp")
                    }))
            except Exception:
                pass
    except WebSocketDisconnect:
        realtime_hub.unregister_websocket(websocket)
    except Exception:
        realtime_hub.unregister_websocket(websocket)

@app.get(f"{api_prefix}/tracking/{{tracking_id}}", tags=["Tracking"])
async def track_application(tracking_id: str):
    """
    Direct tracking lookup by Complaint ID (e.g. CMP-...) or Master Ticket ID (e.g. MST-..., SYN-...).
    """
    result = db.track_by_id(tracking_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Tracking ID '{tracking_id}' not found in municipal records")
    return result

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
