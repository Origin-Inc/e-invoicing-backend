from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers.v1 import health
from fastapi_limiter import FastAPILimiter
from .database import get_supabase_client, test_connection, initialize_storage
import redis.asyncio as redis
import os
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        redis_connection = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis_connection)
        logger.info("Rate limiter initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize rate limiter: {e}")
    
    # Initialize Supabase client
    try:
        client = get_supabase_client()
        logger.info("Supabase client initialized successfully")
        
        # Test database connection
        if test_connection():
            logger.info("✅ Database connection verified")
        else:
            logger.warning("❌ Database connection test failed")
            
        # Initialize storage buckets
        bucket_results = initialize_storage()
        successful_buckets = [name for name, success in bucket_results.items() if success]
        failed_buckets = [name for name, success in bucket_results.items() if not success]
        
        if successful_buckets:
            logger.info(f"✅ Storage buckets ready: {', '.join(successful_buckets)}")
        if failed_buckets:
            logger.warning(f"❌ Storage bucket failures: {', '.join(failed_buckets)}")
        
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
    
    yield
    
    # Shutdown
    try:
        await FastAPILimiter.close()
        logger.info("Rate limiter closed successfully")
    except Exception as e:
        logger.warning(f"Failed to close rate limiter: {e}")

app = FastAPI(
    title="E-Invoicing API",
    description="API for E-Invoicing application with AI-powered features",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/v1", tags=["health"])