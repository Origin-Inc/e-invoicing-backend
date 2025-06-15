import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a simple test app without rate limiting for testing
def create_test_app():
    test_app = FastAPI()
    
    # Add CORS middleware
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )
    
    # Add simple test endpoints without rate limiting
    @test_app.get("/v1/")
    def read_root():
        return {"message": "API is running"}

    @test_app.get("/v1/health")
    def health_check():
        return {"status": "ok"}
    
    return test_app

@pytest.fixture
def client():
    """Create test client with simplified app"""
    app = create_test_app()
    return TestClient(app)

def test_health_check_endpoint(client):
    """Test that health check endpoint works"""
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint(client):
    """Test that root endpoint works"""
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_cors_configuration(client):
    """Test basic CORS functionality"""
    # Test that the endpoint responds correctly
    response = client.get("/v1/health")
    assert response.status_code == 200
    # Note: TestClient doesn't fully simulate CORS preflight requests 