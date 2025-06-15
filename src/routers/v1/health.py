from fastapi import APIRouter
from ...utils.rate_limiting import lenient_rate_limit

router = APIRouter()

# Root endpoint with lenient rate limiting
@router.get("/", dependencies=[lenient_rate_limit()])
def read_root():
    return {"message": "API is running"}

# Health endpoint should not have rate limiting for monitoring
@router.get("/health")
def health_check():
    return {"status": "ok"} 