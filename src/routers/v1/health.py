from fastapi import APIRouter
from ...utils.rate_limiting import lenient_rate_limit
from ...database import get_supabase_client, test_connection, get_storage_service, get_crud_service

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
    
    # Check storage service
    try:
        storage_service = get_storage_service()
        # Test storage by listing buckets (this will fail if storage isn't working)
        buckets = storage_service.client.storage.list_buckets()
        bucket_names = [b.name for b in buckets] if buckets else []
        
        health_status["services"]["storage"] = {
            "status": "healthy",
            "buckets": bucket_names,
            "bucket_types": list(storage_service.buckets.keys())
        }
    except Exception as e:
        health_status["services"]["storage"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Update overall status based on services
    unhealthy_services = [
        name for name, service in health_status["services"].items() 
        if isinstance(service, dict) and service.get("status") == "unhealthy"
    ]
    
    if unhealthy_services:
        health_status["status"] = "degraded"
        health_status["unhealthy_services"] = unhealthy_services
    
    return health_status 