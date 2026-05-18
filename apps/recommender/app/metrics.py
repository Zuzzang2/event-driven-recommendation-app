from prometheus_client import Counter, Histogram

predict_requests_total = Counter(
    "predict_requests_total",
    "추천 요청 수",
    ["status"],
)

predict_latency = Histogram(
    "predict_latency_seconds",
    "추천 응답 지연시간 (inference latency)",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)
