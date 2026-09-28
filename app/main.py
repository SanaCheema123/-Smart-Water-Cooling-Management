from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routers import health, readings, analytics, websocket

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        app.state.database_ready = True
    except Exception as exc:
        app.state.database_ready = False
        print(f"WARNING: PostgreSQL is not available yet: {exc.__class__.__name__}: {exc}")
    yield

app = FastAPI(
    title="Smart Water and Cooling Management Platform",
    version="1.1.0",
    description="Real-time water monitoring, cooling-demand prediction, leak/anomaly detection, WUE, weather-aware recommendations, WebSockets, PostgreSQL and Grafana.",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(readings.router)
app.include_router(analytics.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"project": "Smart Water and Cooling Management Platform", "version": "1.1.0", "status": "running", "docs": "/docs", "websocket": "/ws/sensors"}
