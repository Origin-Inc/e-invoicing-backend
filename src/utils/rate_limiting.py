from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

# Different rate limiting configurations for different endpoint types
def strict_rate_limit():
    """For sensitive operations like authentication"""
    return Depends(RateLimiter(times=5, seconds=60))

def moderate_rate_limit():
    """For general API endpoints"""
    return Depends(RateLimiter(times=30, seconds=60))

def lenient_rate_limit():
    """For less sensitive endpoints"""
    return Depends(RateLimiter(times=100, seconds=60))

# No rate limiting for health checks and monitoring endpoints 