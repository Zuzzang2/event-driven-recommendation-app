# event-driven-recommendation-app TODO

## Week 1 — 애플리케이션 코어

### event-collector
- [x] `apps/event-collector/` 디렉토리 구조 생성
- [x] `requirements.txt` 작성 (fastapi, uvicorn, asyncpg, prometheus-client)
- [x] `db/database.py` — asyncpg 연결 풀
- [x] `models/event.py` — Pydantic EventCreate, EventResponse
- [x] `api/events.py` — POST /events 라우터
- [x] `main.py` — FastAPI 앱, GET /health, GET /metrics
- [x] `metrics.py` — Counter: event_collect_requests_total
- [x] `Dockerfile` 작성 (linux/arm64 대응)

### recommender
- [x] `apps/recommender/` 디렉토리 구조 생성
- [x] `requirements.txt` 작성
- [x] `db/database.py` — asyncpg 연결 풀
- [x] `api/predict.py` — GET /predict/{user_id} 라우터
- [x] `main.py` — FastAPI 앱, GET /health, GET /metrics
- [x] `metrics.py` — Histogram: predict_latency_seconds
- [x] `Dockerfile` 작성

### recommender-job
- [x] `apps/recommender-job/` 디렉토리 구조 생성
- [x] `requirements.txt` 작성 (asyncpg)
- [x] `job.py` — events 집계 → recommendations UPSERT 쿼리
- [x] `Dockerfile` 작성

### DB 마이그레이션
- [x] `migrations/` 설정 (Alembic + psycopg2)
- [x] `migrations/versions/001_create_tables.py` — events, recommendations 테이블 생성
- [x] Supabase에 마이그레이션 적용 완료

---

## Week 2 — CI/CD

### GitHub Actions CI
- [ ] `.github/workflows/ci-event-collector.yaml`
  - [ ] push 트리거 (apps/event-collector/** 변경 시)
  - [ ] docker buildx (linux/arm64)
  - [ ] ghcr.io push
  - [ ] repository_dispatch → infra repo
- [ ] `.github/workflows/ci-recommender.yaml`
- [ ] `.github/workflows/ci-recommender-job.yaml`

### GitHub 설정
- [ ] ghcr.io 패키지 퍼블릭 설정
- [ ] `INFRA_REPO_TOKEN` Secret 등록 (repository_dispatch용)

---

## Week 3 — 검증

- [ ] CI 전체 흐름 end-to-end 확인 (push → 이미지 빌드 → infra dispatch)
