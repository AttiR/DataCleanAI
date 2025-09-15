from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict, deque
from typing import Dict, Deque

# In-memory rate limiting (for production, use Redis)
rate_limit_storage: Dict[str, Deque[float]] = defaultdict(lambda: deque())

class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window

    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed based on rate limit."""
        now = time.time()
        window_start = now - self.time_window

        # Get or create request history for this key
        requests = rate_limit_storage[key]

        # Remove old requests outside the time window
        while requests and requests[0] < window_start:
            requests.popleft()

        # Check if we're under the limit
        if len(requests) >= self.max_requests:
            return False

        # Add current request
        requests.append(now)
        return True

    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests in current time window."""
        now = time.time()
        window_start = now - self.time_window

        requests = rate_limit_storage[key]

        # Remove old requests
        while requests and requests[0] < window_start:
            requests.popleft()

        return max(0, self.max_requests - len(requests))

    def get_reset_time(self, key: str) -> float:
        """Get time when rate limit resets."""
        if not rate_limit_storage[key]:
            return time.time()

        oldest_request = min(rate_limit_storage[key])
        return oldest_request + self.time_window

# Rate limiters for different endpoints
login_rate_limiter = RateLimiter(max_requests=5, time_window=300)  # 5 attempts per 5 minutes
register_rate_limiter = RateLimiter(max_requests=3, time_window=3600)  # 3 registrations per hour
password_reset_rate_limiter = RateLimiter(max_requests=3, time_window=3600)  # 3 resets per hour
general_rate_limiter = RateLimiter(max_requests=100, time_window=60)  # 100 requests per minute

def get_client_ip(request: Request) -> str:
    """Get client IP address from request."""
    # Check for forwarded headers first
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fallback to direct connection
    return request.client.host if request.client else "unknown"

def check_rate_limit(request: Request, limiter: RateLimiter) -> None:
    """Check rate limit and raise exception if exceeded."""
    client_ip = get_client_ip(request)

    if not limiter.is_allowed(client_ip):
        reset_time = limiter.get_reset_time(client_ip)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "retry_after": int(reset_time - time.time()),
                "remaining": limiter.get_remaining_requests(client_ip)
            }
        )

def rate_limit_response(limiter: RateLimiter, client_ip: str) -> JSONResponse:
    """Create rate limit response with headers."""
    remaining = limiter.get_remaining_requests(client_ip)
    reset_time = limiter.get_reset_time(client_ip)

    headers = {
        "X-RateLimit-Limit": str(limiter.max_requests),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(int(reset_time)),
        "Retry-After": str(int(reset_time - time.time()))
    }

    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "retry_after": int(reset_time - time.time()),
            "remaining": remaining
        },
        headers=headers
    )
