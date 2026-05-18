from fastapi import APIRouter, HTTPException
from app.db.database import get_pool
from app.metrics import events_total
from app.models.event import EventCreate, EventResponse

router = APIRouter()


@router.post("/events", response_model=EventResponse, status_code=201)
async def collect_event(event: EventCreate):
    pool = get_pool()
    row = await pool.fetchrow(
        """
        INSERT INTO events (user_id, item_id, event_type)
        VALUES ($1, $2, $3)
        RETURNING id, user_id, item_id, event_type
        """,
        event.user_id,
        event.item_id,
        event.event_type,
    )
    if not row:
        raise HTTPException(status_code=500, detail="insert failed")
    events_total.labels(event_type=event.event_type).inc()
    return dict(row)
