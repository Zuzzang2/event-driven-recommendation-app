import asyncio
import asyncpg
import os
import time


SCORE_UPSERT_SQL = """
INSERT INTO recommendations (user_id, item_id, score, computed_at)
SELECT
    user_id,
    item_id,
    SUM(CASE event_type WHEN 'click' THEN 3.0 WHEN 'view' THEN 1.0 END)
        / (EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 3600 + 1),
    NOW()
FROM events
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY user_id, item_id
ON CONFLICT (user_id, item_id) DO UPDATE
    SET score       = EXCLUDED.score,
        computed_at = EXCLUDED.computed_at
"""


async def run():
    start = time.perf_counter()
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])
    try:
        result = await conn.execute(SCORE_UPSERT_SQL)
        # result 형식: "INSERT 0 N"
        count = int(result.split()[-1])
        duration = time.perf_counter() - start
        print(f"[recommender-job] upserted={count} rows, duration={duration:.3f}s")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run())
