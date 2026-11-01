import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Set
from collections import deque
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class RealtimeHub:
    """
    Central Real-Time Event Hub for SamAashwas Civic Platform.
    Manages active WebSockets and Server-Sent Event (SSE) subscribers.
    Provides sub-50ms event broadcasting for citizen complaints, fleet movements,
    AI verification passes, and contractor audits.
    """

    def __init__(self, max_history: int = 100):
        self.active_websockets: Set[WebSocket] = set()
        self.sse_queues: Set[asyncio.Queue] = set()
        self.event_history: deque = deque(maxlen=max_history)
        self.is_telemetry_running: bool = False
        self._background_task: asyncio.Task = None

        # Municipal fleet simulation initial positions
        self.fleet_squads = [
            {"id": "SQD-BLR-01", "name": "Squad Alpha-1 (Pothole Rapid Patch)", "city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "status": "ON_PATROL", "speed_kmh": 28, "heading": 45},
            {"id": "SQD-BLR-02", "name": "Squad Bravo-2 (Jetting & Desilting)", "city": "Bengaluru", "lat": 12.9352, "lon": 77.6245, "status": "EN_ROUTE", "speed_kmh": 32, "heading": 120},
            {"id": "SQD-DEL-01", "name": "Squad Delta-4 (Transformer Restorations)", "city": "Delhi", "lat": 28.6508, "lon": 77.1906, "status": "SITE_ACTIVE", "speed_kmh": 0, "heading": 0},
            {"id": "SQD-MUM-01", "name": "Squad Echo-5 (Storm Drain Cleansing)", "city": "Mumbai", "lat": 19.0596, "lon": 72.8295, "status": "ON_PATROL", "speed_kmh": 22, "heading": 210}
        ]

    async def register_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.active_websockets.add(websocket)
        logger.info(f"WebSocket client connected. Active connections: {len(self.active_websockets)}")
        # Send connection handshake and recent event history
        handshake = {
            "type": "CONNECTION_ESTABLISHED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "Connected to SamAashwas Real-Time Civic Stream",
            "server_time_ist": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S IST"),
            "active_clients": len(self.active_websockets)
        }
        await websocket.send_text(json.dumps(handshake))

        # Replay last 8 events
        recent = list(self.event_history)[-8:]
        for ev in recent:
            try:
                await websocket.send_text(json.dumps(ev))
            except Exception:
                break

    def unregister_websocket(self, websocket: WebSocket):
        if websocket in self.active_websockets:
            self.active_websockets.remove(websocket)
            logger.info(f"WebSocket client disconnected. Active connections: {len(self.active_websockets)}")

    def register_sse(self) -> asyncio.Queue:
        q = asyncio.Queue(maxsize=100)
        self.sse_queues.add(q)
        logger.info(f"SSE client registered. Active queues: {len(self.sse_queues)}")
        return q

    def unregister_sse(self, q: asyncio.Queue):
        if q in self.sse_queues:
            self.sse_queues.remove(q)
            logger.info(f"SSE client removed. Active queues: {len(self.sse_queues)}")

    async def broadcast(self, event_type: str, data: Dict[str, Any]):
        """
        Broadcasts an event payload to all connected WebSockets and SSE streams.
        """
        event_packet = {
            "event_id": f"EVT-{uuid.uuid4().hex[:8].upper()}",
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
        self.event_history.append(event_packet)
        message_json = json.dumps(event_packet)

        # Broadcast to WebSockets
        dead_ws = []
        for ws in self.active_websockets:
            try:
                await ws.send_text(message_json)
            except Exception:
                dead_ws.append(ws)
        for ws in dead_ws:
            self.unregister_websocket(ws)

        # Broadcast to SSE Queues
        dead_sse = []
        for q in self.sse_queues:
            try:
                q.put_nowait(event_packet)
            except asyncio.QueueFull:
                pass
            except Exception:
                dead_sse.append(q)
        for q in dead_sse:
            self.unregister_sse(q)

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self.event_history)

    async def telemetry_background_loop(self):
        """
        Background task that runs continuously during server lifespan:
        - Simulates live squad movement on urban road grids
        - Emits live civic activity pulses and weather updates
        """
        self.is_telemetry_running = True
        logger.info("Real-time telemetry background loop started.")
        step = 0

        while self.is_telemetry_running:
            try:
                await asyncio.sleep(3.5)
                step += 1

                # 1. Update fleet squad coordinates slightly along circular/street path
                for sq in self.fleet_squads:
                    if sq["status"] in ["ON_PATROL", "EN_ROUTE"]:
                        delta_lat = (0.0003 * ((step % 6) - 2.5)) * 0.4
                        delta_lon = (0.0003 * (((step + 2) % 6) - 2.5)) * 0.4
                        sq["lat"] = round(sq["lat"] + delta_lat, 6)
                        sq["lon"] = round(sq["lon"] + delta_lon, 6)
                        sq["speed_kmh"] = round(20 + (step % 15) * 1.5, 1)

                await self.broadcast("FLEET_TELEMETRY_PULSE", {
                    "squads": self.fleet_squads,
                    "tick": step,
                    "active_squad_count": len(self.fleet_squads)
                })

                # 2. Every 7 seconds emit a live civic pulse event
                if step % 2 == 0:
                    sample_events = [
                        {"action": "AI_DEDUPLICATION_MERGE", "message": "Cluster MST-0E08F041 in Ward 112 absorbed new duplicate complaint (+1 urgency upvote)", "ward": "Ward 112 (Domlur)", "city": "Bengaluru"},
                        {"action": "SLA_COUNTDOWN_TICK", "message": "High-urgency watermain leak in Karol Bagh assigned to JE repair squad under 4-hour statutory SLA", "ward": "Karol Bagh Zone", "city": "Delhi"},
                        {"action": "HOMOGRAPHY_AUTO_AUDITED", "message": "Computer vision verified asphalt plate compaction. Clause 14B escrow compliance confirmed", "ward": "Indiranagar (Ward 1)", "city": "Bengaluru"},
                        {"action": "IVR_CALL_RESOLVED", "message": "1913 Toll-Free Vernacular helpline ingested Bhojpuri complaint from Gorakhpur citizen via Bhashini ASR", "ward": "Ward 18", "city": "Lucknow"},
                        {"action": "CITIZEN_KARMA_UNLOCKED", "message": "Citizen Rajesh Kumar earned +100 Swachh Nagrik points for confirming road restoration", "ward": "Domlur", "city": "Bengaluru"}
                    ]
                    chosen = sample_events[(step // 2) % len(sample_events)]
                    await self.broadcast("CIVIC_ACTIVITY_STREAM_EVENT", chosen)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in telemetry loop: {e}")
                await asyncio.sleep(2)

        logger.info("Real-time telemetry background loop stopped.")

# Singleton RealtimeHub instance
realtime_hub = RealtimeHub()
