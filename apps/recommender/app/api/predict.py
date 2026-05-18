import time
from fastapi import APIRouter
from app.db.database import get_pool
from app.metrics import predict_requests_total, predict_latency

router = APIRouter()


@router.get("/predict/{user_id}")
async def predict(user_id: str):
    start = time.perf_counter()
    pool = get_pool()
    rows = await pool.fetch(
        """
        SELECT item_id, score
        FROM recommendations
        WHERE user_id = $1
        ORDER BY score DESC
        LIMIT 10
        """,
        user_id,
    )
    duration = time.perf_counter() - start
    predict_latency.observe(duration)
    predict_requests_total.labels(status="200").inc()
    return {
        "user_id": user_id,
        "recommendations": [dict(r) for r in rows],
    }
