# event-driven-recommendation-app TODO

## 애플리케이션 코어

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

## CI/CD

### GitHub Actions CI
- [x] `.github/workflows/build-push.yaml` — 재사용 워크플로우 (빌드/push 공통 로직)
- [x] `.github/workflows/ci-event-collector.yaml`
  - [x] push 트리거 (apps/event-collector/** 변경 시)
  - [x] docker buildx (linux/arm64)
  - [x] ghcr.io push
  - ~~repository_dispatch → infra repo~~ — 의도적 미진행 (배포는 infra 수동 Sync)
- [x] `.github/workflows/ci-recommender.yaml`
- [x] `.github/workflows/ci-recommender-job.yaml`

### GitHub 설정
- [x] ghcr.io 패키지 퍼블릭 설정
- ~~`INFRA_REPO_TOKEN` Secret (repository_dispatch용)~~ — 미진행 (CD 자동화 안 함)

---

## 검증

- [x] CI 전체 흐름 확인 (push → 이미지 빌드 → ghcr push)
- [ ] end-to-end: 이미지 태그 갱신 → ArgoCD 수동 Sync → 배포 확인
