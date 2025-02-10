from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response
from functools import wraps
import time
import logging

# Initialize metrics
REQUEST_COUNT = Counter(
    'text_to_sql_requests_total',
    'Total number of SQL generation requests',
    ['status']
)

REQUEST_LATENCY = Histogram(
    'text_to_sql_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

logger = logging.getLogger(__name__)

def init_metrics(app: FastAPI):
    """Initialize metrics endpoints"""
    
    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type="text/plain"
        )

def track_request_time(func):
    """Decorator to track request timing"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            REQUEST_COUNT.labels(status="success").inc()
            return result
            
        except Exception as e:
            REQUEST_COUNT.labels(status="error").inc()
            raise
            
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(
                endpoint=func.__name__
            ).observe(duration)
            
    return wrapper
