from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers.v1 import health
from fastapi_limiter import FastAPILimiter
from .database import get_supabase_client, test_connection
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
        # Continue without rate limiting in development
    
    # Initialize Supabase connection
    try:
        supabase_client = get_supabase_client()
        if test_connection():
            logger.info(f"Supabase connected successfully to {supabase_client.supabase_url}")
        else:
            logger.warning("Supabase connection test failed")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
        # Continue without Supabase in development if needed
    
    yield
    
    # Shutdown
    try:
        await FastAPILimiter.close()
    except:
        pass

app = FastAPI(lifespan=lifespan)

# CORS Middleware - More restrictive for production
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Configurable origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Specific methods
    allow_headers=["*"],  # Can be more restrictive in production
)

app.include_router(health.router, prefix="/v1", tags=["health"])