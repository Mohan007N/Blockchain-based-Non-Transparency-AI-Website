"""
Monitoring middleware for Prometheus metrics
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge
from app.config.settings import settings

logger = logging.getLogger("verity-ai.monitoring")

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Number of active HTTP requests'
)

VERIFICATION_COUNT = Counter(
    'verifications_total',
    'Total loan verifications',
    ['loan_type', 'status']
)

BLOCKCHAIN_TRANSACTIONS = Counter(
    'blockchain_transactions_total',
    'Total blockchain transactions',
    ['status']
)

WEBSOCKET_CONNECTIONS = Gauge(
    'websocket_connections_active',
    'Number of active WebSocket connections'
)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to collect metrics for all requests"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)
        
        # Track active requests
        ACTIVE_REQUESTS.inc()
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Add custom headers
            response.headers["X-Process-Time"] = str(duration)
            
            return response
            
        except Exception as e:
            # Record error
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            
            logger.error(f"Request failed: {e}")
            raise
            
        finally:
            # Decrement active requests
            ACTIVE_REQUESTS.dec()


def track_verification(loan_type: str, status: str):
    """Track verification metrics"""
    VERIFICATION_COUNT.labels(
        loan_type=loan_type,
        status=status
    ).inc()


def track_blockchain_transaction(status: str):
    """Track blockchain transaction metrics"""
    BLOCKCHAIN_TRANSACTIONS.labels(status=status).inc()


def update_websocket_connections(count: int):
    """Update WebSocket connection count"""
    WEBSOCKET_CONNECTIONS.set(count)
