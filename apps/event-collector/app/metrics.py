from prometheus_client import Counter

events_total = Counter(
    "event_collect_requests_total",
    "수집된 이벤트 수",
    ["event_type"],
)
