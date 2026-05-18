# event-driven-recommendation-app

유저 행동 기반 추천 시스템 — 애플리케이션 서비스 레포

## 프로젝트 개요

이벤트 수집 → 배치 점수 계산 → 추천 서빙으로 이어지는 MLOps 파이프라인을 DevOps 관점으로 구성한 포트폴리오 프로젝트.
ML 20% / DevOps 80% 비중. 복잡한 ML 알고리즘 없이 SQL 기반 popularity score로 추천.

## 기술 스택

| 영역 | 기술 |
|------|------|
| API | FastAPI (Python, asyncpg) |
| DB | Supabase (외부 관리형 PostgreSQL) |
| Container Registry | ghcr.io |
| CI | GitHub Actions (docker buildx, linux/arm64) |

## 서비스 구조

```
apps/
├── event-collector/    # POST /events — 클릭/조회 이벤트 수집 → Supabase events 테이블
├── recommender/        # GET /predict/{user_id} — recommendations 테이블 조회 후 반환
└── recommender-job/    # 배치 스크립트 — K8s CronJob으로 실행, 점수 계산 후 UPSERT
```

## DB 스키마 (Supabase)

```sql
-- 이벤트 수집
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    item_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(20) NOT NULL,  -- 'view' | 'click'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 배치 점수 계산 결과 캐시
CREATE TABLE recommendations (
    user_id VARCHAR(50) NOT NULL,
    item_id VARCHAR(50) NOT NULL,
    score FLOAT NOT NULL,
    computed_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, item_id)
);
```

## 추천 점수 알고리즘

click 가중치 3, view 가중치 1, 시간 감쇠 적용, 7일 윈도우.
복잡한 ML 없이 SQL UPSERT로 처리 (recommender-job/job.py).

## CI/CD 흐름

```
git push main (apps/** 변경)
  → GitHub Actions CI
    → docker buildx --platform linux/arm64
    → ghcr.io/Zuzzang2/{service}:{git-sha} push
    → repository_dispatch → event-driven-recommendation-infra
```

## Prometheus 메트릭

| 메트릭 | 타입 | 위치 |
|--------|------|------|
| `event_collect_requests_total` | Counter | event-collector |
| `predict_requests_total` | Counter | recommender |
| `predict_latency_seconds` | Histogram | recommender |
| `recommender_job_duration_seconds` | Gauge | recommender-job |

## 주요 규칙

- Dockerfile은 반드시 `linux/arm64` 플랫폼 대응 (EC2 t4g.large ARM 인스턴스)
- DB 연결은 `DATABASE_URL` 환경변수 단일 진입점으로 통일
- 시크릿은 `.env`에만, `.env`는 절대 커밋하지 않음
- `Co-Authored-By` 커밋 라인 추가 금지

## 작업 완료 규칙

**어떤 작업을 완료했다면 반드시 `todo.md`의 해당 항목을 `[x]`로 체크한 뒤 다음 작업으로 넘어간다.**
