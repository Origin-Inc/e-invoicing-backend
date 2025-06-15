"""Database module for E-Invoicing application."""

from .supabase_client import get_supabase_client, supabase, test_connection

__all__ = ["get_supabase_client", "supabase", "test_connection"] 