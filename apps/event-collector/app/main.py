from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api.events import router
from app.db.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(title="event-collector", lifespan=lifespan)
app.include_router(router)
app.mount("/metrics", make_asgi_app())


@app.get("/health")
async def health():
    return {"status": "ok"}
