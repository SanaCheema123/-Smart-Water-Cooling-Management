from fastapi import WebSocket

clients: set[WebSocket] = set()

async def connect(ws: WebSocket):
    await ws.accept()
    clients.add(ws)

def disconnect(ws: WebSocket):
    clients.discard(ws)

async def broadcast(payload: dict):
    dead = []
    for ws in list(clients):
        try:
            await ws.send_json(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        clients.discard(ws)
