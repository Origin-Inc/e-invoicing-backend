"""Supabase client configuration for E-Invoicing application."""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Global Supabase client instance
supabase: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create a Supabase client instance.
    
    Returns:
        Client: Configured Supabase client
        
    Raises:
        ValueError: If required environment variables are not set
    """
    global supabase
    
    if supabase is not None:
        return supabase
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
        )
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as e:
        raise ConnectionError(f"Failed to create Supabase client: {str(e)}")


def get_service_role_client() -> Client:
    """
    Get a Supabase client with service role key for admin operations.
    
    Returns:
        Client: Supabase client with service role permissions
        
    Raises:
        ValueError: If service role key is not set
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables must be set"
        )
    
    try:
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    except Exception as e:
        raise ConnectionError(f"Failed to create Supabase service role client: {str(e)}")


def test_connection() -> bool:
    """
    Test the Supabase connection.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        client = get_supabase_client()
        # Try a simple query to test the connection
        # This will fail gracefully if there are no tables yet
        response = client.auth.get_session()
        return True
    except Exception as e:
        print(f"Supabase connection test failed: {str(e)}")
        return False 