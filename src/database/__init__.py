"""Database module for E-Invoicing application."""

from .supabase_client import get_supabase_client, supabase, test_connection
from .storage import get_storage_service, initialize_storage, StorageService
from .crud import get_crud_service, CRUDService
from .models import (
    Client, ClientCreate, ClientUpdate, ClientResponse,
    Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse,
    Payment, PaymentCreate, PaymentUpdate,
    InvoiceStatus, PaymentStatus, PaginatedResponse,
    InvoiceItem
)

__all__ = [
    # Supabase client
    "get_supabase_client", 
    "supabase", 
    "test_connection",
    
    # Storage service
    "get_storage_service",
    "initialize_storage", 
    "StorageService",
    
    # CRUD service
    "get_crud_service",
    "CRUDService",
    
    # Models
    "Client", "ClientCreate", "ClientUpdate", "ClientResponse",
    "Invoice", "InvoiceCreate", "InvoiceUpdate", "InvoiceResponse",
    "Payment", "PaymentCreate", "PaymentUpdate",
    "InvoiceStatus", "PaymentStatus", "PaginatedResponse",
    "InvoiceItem"
] 