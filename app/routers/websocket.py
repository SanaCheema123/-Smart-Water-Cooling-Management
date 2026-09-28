from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.broadcast import connect, disconnect

router = APIRouter(tags=["Realtime"])

@router.websocket("/ws/sensors")
async def sensor_socket(ws: WebSocket):
    await connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        disconnect(ws)
    except Exception:
        disconnect(ws)
