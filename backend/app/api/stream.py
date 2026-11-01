import json
import asyncio
from typing import Optional, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse
from ..core.realtime import realtime_hub

router = APIRouter(prefix="/stream", tags=["Real-Time Event Stream"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Bi-directional real-time WebSocket connection for live telemetry,
    instant complaint broadcasts, and citizen presence events.
    """
    await realtime_hub.register_websocket(websocket)
    try:
        while True:
            # Keep connection open & handle incoming client messages/pings
            data_text = await websocket.receive_text()
            try:
                msg = json.loads(data_text)
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

@router.get("/events", summary="Server-Sent Events (SSE) live event stream")
async def sse_event_stream(request: Request):
    """
    Continuous Server-Sent Events (SSE) stream for low-overhead HTTP real-time updates.
    """
    async def event_generator():
        q = realtime_hub.register_sse()
        try:
            # Initial connection packet
            yield f"data: {json.dumps({'type': 'SSE_CONNECTED', 'message': 'Live stream active'})}\n\n"
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(q.get(), timeout=20.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat comment
                    yield f": keep-alive\n\n"
        finally:
            realtime_hub.unregister_sse(q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/history", summary="Recent real-time events buffer")
async def get_recent_stream_history():
    """
    Returns the recent buffered real-time events for immediate catch-up.
    """
    return {
        "total_buffered": len(realtime_hub.event_history),
        "events": realtime_hub.get_history()
    }

@router.post("/broadcast-test", summary="Test broadcast trigger")
async def broadcast_test_event(payload: Dict[str, Any]):
    """
    Allows emitting a real-time event for testing.
    """
    ev_type = payload.get("type", "SYSTEM_TEST_EVENT")
    ev_data = payload.get("data", {"message": "Test real-time broadcast"})
    await realtime_hub.broadcast(ev_type, ev_data)
    return {"status": "broadcasted", "type": ev_type}
