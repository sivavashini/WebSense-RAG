from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from routes import chat, health, history, reports, upload
from services.config import settings
from services.database import init_db
from services.websocket import manager

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(
    title="WebSense RAG API",
    description="Responsibility-focused RAG assistant with SpideySense risk analysis.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
    allow_origin_regex=settings.frontend_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Let your SpideySense cool down."})


@app.on_event("startup")
async def startup():
    await init_db()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/api/ws")
async def websocket_api_endpoint(websocket: WebSocket):
    # Vercel deployment: frontend connects to the backend through the /api route prefix.
    await websocket_endpoint(websocket)


app.include_router(health.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(history.router)
app.include_router(reports.router)

# Vercel deployment: Services route the backend under /api. Registering both
# unprefixed and prefixed routes keeps local uvicorn, Vite proxy, and Vercel routing compatible.
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
