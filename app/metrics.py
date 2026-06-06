from fastapi import APIRouter, Depends
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.auth import get_admin_agent

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests")
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency")

router = APIRouter()


@router.get("/metrics", dependencies=[Depends(get_admin_agent)])
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)