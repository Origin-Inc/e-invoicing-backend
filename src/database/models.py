"""Database models for E-Invoicing application."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
import uuid

# Enums for status fields
class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

# Base model with common fields
class BaseDBModel(BaseModel):
    """Base model with common database fields."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# User/Client models
class Client(BaseDBModel):
    """Client/Customer model."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    is_active: bool = True

class ClientCreate(BaseModel):
    """Model for creating a new client."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)

class ClientUpdate(BaseModel):
    """Model for updating a client."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

# Invoice models
class InvoiceItem(BaseModel):
    """Individual item in an invoice."""
    description: str = Field(..., min_length=1, max_length=500)
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    total: float = Field(..., ge=0)

class Invoice(BaseDBModel):
    """Invoice model."""
    invoice_number: str = Field(..., min_length=1, max_length=50)
    client_id: str
    client_name: Optional[str] = None  # Denormalized for easier queries
    client_email: Optional[str] = None  # Denormalized for easier queries
    
    # Invoice details
    issue_date: datetime
    due_date: datetime
    status: InvoiceStatus = InvoiceStatus.DRAFT
    
    # Financial details
    subtotal: float = Field(..., ge=0)
    tax_rate: float = Field(default=0.0, ge=0, le=1)
    tax_amount: float = Field(..., ge=0)
    discount_amount: float = Field(default=0.0, ge=0)
    total_amount: float = Field(..., ge=0)
    
    # Items and notes
    items: List[InvoiceItem] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=1000)
    terms: Optional[str] = Field(None, max_length=1000)
    
    # File attachments
    pdf_url: Optional[str] = None
    attachment_urls: List[str] = Field(default_factory=list)

class InvoiceCreate(BaseModel):
    """Model for creating a new invoice."""
    client_id: str
    issue_date: datetime
    due_date: datetime
    items: List[InvoiceItem] = Field(..., min_items=1)
    tax_rate: float = Field(default=0.0, ge=0, le=1)
    discount_amount: float = Field(default=0.0, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    terms: Optional[str] = Field(None, max_length=1000)

class InvoiceUpdate(BaseModel):
    """Model for updating an invoice."""
    client_id: Optional[str] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[InvoiceStatus] = None
    items: Optional[List[InvoiceItem]] = None
    tax_rate: Optional[float] = Field(None, ge=0, le=1)
    discount_amount: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    terms: Optional[str] = Field(None, max_length=1000)
    pdf_url: Optional[str] = None
    attachment_urls: Optional[List[str]] = None

# Payment models
class Payment(BaseDBModel):
    """Payment model."""
    invoice_id: str
    amount: float = Field(..., gt=0)
    payment_date: datetime
    payment_method: str = Field(..., max_length=50)
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)

class PaymentCreate(BaseModel):
    """Model for creating a new payment."""
    invoice_id: str
    amount: float = Field(..., gt=0)
    payment_date: datetime
    payment_method: str = Field(..., max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)

class PaymentUpdate(BaseModel):
    """Model for updating a payment."""
    amount: Optional[float] = Field(None, gt=0)
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = Field(None, max_length=50)
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)

# Response models for API
class PaginatedResponse(BaseModel):
    """Generic paginated response model."""
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int

class ClientResponse(Client):
    """Client response model with computed fields."""
    total_invoices: Optional[int] = 0
    total_amount_due: Optional[float] = 0.0

class InvoiceResponse(Invoice):
    """Invoice response model with computed fields."""
    payment_status: Optional[PaymentStatus] = None
    amount_paid: Optional[float] = 0.0
    amount_due: Optional[float] = None

# Database table schemas (for Supabase table creation)
CLIENT_TABLE_SCHEMA = {
    "table_name": "clients",
    "columns": {
        "id": "uuid PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "varchar(255) NOT NULL",
        "email": "varchar(255) NOT NULL UNIQUE",
        "phone": "varchar(20)",
        "address": "text",
        "city": "varchar(100)",
        "state": "varchar(100)",
        "zip_code": "varchar(20)",
        "country": "varchar(100)",
        "tax_id": "varchar(50)",
        "is_active": "boolean DEFAULT true",
        "created_at": "timestamp with time zone DEFAULT now()",
        "updated_at": "timestamp with time zone DEFAULT now()"
    }
}

INVOICE_TABLE_SCHEMA = {
    "table_name": "invoices",
    "columns": {
        "id": "uuid PRIMARY KEY DEFAULT gen_random_uuid()",
        "invoice_number": "varchar(50) NOT NULL UNIQUE",
        "client_id": "uuid NOT NULL REFERENCES clients(id)",
        "client_name": "varchar(255)",
        "client_email": "varchar(255)",
        "issue_date": "timestamp with time zone NOT NULL",
        "due_date": "timestamp with time zone NOT NULL",
        "status": "varchar(20) DEFAULT 'draft'",
        "subtotal": "decimal(10,2) NOT NULL",
        "tax_rate": "decimal(5,4) DEFAULT 0.0",
        "tax_amount": "decimal(10,2) NOT NULL",
        "discount_amount": "decimal(10,2) DEFAULT 0.0",
        "total_amount": "decimal(10,2) NOT NULL",
        "items": "jsonb NOT NULL",
        "notes": "text",
        "terms": "text",
        "pdf_url": "text",
        "attachment_urls": "jsonb DEFAULT '[]'",
        "created_at": "timestamp with time zone DEFAULT now()",
        "updated_at": "timestamp with time zone DEFAULT now()"
    }
}

PAYMENT_TABLE_SCHEMA = {
    "table_name": "payments",
    "columns": {
        "id": "uuid PRIMARY KEY DEFAULT gen_random_uuid()",
        "invoice_id": "uuid NOT NULL REFERENCES invoices(id)",
        "amount": "decimal(10,2) NOT NULL",
        "payment_date": "timestamp with time zone NOT NULL",
        "payment_method": "varchar(50) NOT NULL",
        "status": "varchar(20) DEFAULT 'pending'",
        "transaction_id": "varchar(100)",
        "notes": "text",
        "created_at": "timestamp with time zone DEFAULT now()",
        "updated_at": "timestamp with time zone DEFAULT now()"
    }
} 