from fastapi import APIRouter
from ...utils.rate_limiting import lenient_rate_limit
from ...database import get_supabase_client, test_connection

router = APIRouter()

# Root endpoint with lenient rate limiting
@router.get("/", dependencies=[lenient_rate_limit()])
def read_root():
    return {"message": "API is running"}

# Health endpoint should not have rate limiting for monitoring
@router.get("/health")
def health_check():
    health_status = {
        "status": "ok",
        "services": {
            "api": "healthy"
        }
    }
    
    # Check database connectivity
    try:
        supabase_client = get_supabase_client()
        db_healthy = test_connection()
        health_status["services"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "url": supabase_client.supabase_url
        }
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status 