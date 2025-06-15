"""CRUD operations for E-Invoicing application using Supabase."""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import logging
from supabase import Client
from .supabase_client import get_supabase_client
from .models import (
    Client as ClientModel, ClientCreate, ClientUpdate, ClientResponse,
    Invoice as InvoiceModel, InvoiceCreate, InvoiceUpdate, InvoiceResponse,
    Payment as PaymentModel, PaymentCreate, PaymentUpdate,
    InvoiceStatus, PaymentStatus, PaginatedResponse
)

logger = logging.getLogger(__name__)

class CRUDService:
    """Service class for CRUD operations using Supabase."""
    
    def __init__(self, client: Optional[Client] = None):
        """
        Initialize the CRUD Service.
        
        Args:
            client: Optional Supabase client instance. If not provided, 
                   will use the default client.
        """
        self.client = client or get_supabase_client()
    
    # Client CRUD operations
    def create_client(self, client_data: ClientCreate) -> Optional[ClientModel]:
        """
        Create a new client.
        
        Args:
            client_data: Client creation data
            
        Returns:
            Created client or None if failed
        """
        try:
            # Convert Pydantic model to dict
            data = client_data.model_dump()
            
            # Insert into database
            response = self.client.table("clients").insert(data).execute()
            
            if response.data:
                client_dict = response.data[0]
                return ClientModel(**client_dict)
            
            logger.error(f"Failed to create client: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error creating client: {e}")
            return None
    
    def get_client(self, client_id: str) -> Optional[ClientResponse]:
        """
        Get a client by ID with computed fields.
        
        Args:
            client_id: Client ID
            
        Returns:
            Client with computed fields or None if not found
        """
        try:
            # Get client data
            response = self.client.table("clients").select("*").eq("id", client_id).execute()
            
            if not response.data:
                return None
            
            client_dict = response.data[0]
            
            # Get computed fields (total invoices and amount due)
            invoice_stats = self.client.table("invoices").select(
                "id, total_amount, status"
            ).eq("client_id", client_id).execute()
            
            total_invoices = len(invoice_stats.data) if invoice_stats.data else 0
            total_amount_due = sum(
                float(inv.get("total_amount", 0)) 
                for inv in invoice_stats.data or []
                if inv.get("status") in ["sent", "overdue"]
            )
            
            # Create response model
            client_dict.update({
                "total_invoices": total_invoices,
                "total_amount_due": total_amount_due
            })
            
            return ClientResponse(**client_dict)
            
        except Exception as e:
            logger.error(f"Error getting client {client_id}: {e}")
            return None
    
    def get_clients(
        self, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> PaginatedResponse:
        """
        Get paginated list of clients.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active clients
            
        Returns:
            Paginated response with clients
        """
        try:
            # Build query
            query = self.client.table("clients").select("*", count="exact")
            
            if active_only:
                query = query.eq("is_active", True)
            
            # Apply pagination
            query = query.range(skip, skip + limit - 1).order("created_at", desc=True)
            
            response = query.execute()
            
            clients = [ClientModel(**client) for client in response.data or []]
            total = response.count or 0
            
            return PaginatedResponse(
                items=clients,
                total=total,
                page=(skip // limit) + 1,
                per_page=limit,
                pages=(total + limit - 1) // limit
            )
            
        except Exception as e:
            logger.error(f"Error getting clients: {e}")
            return PaginatedResponse(items=[], total=0, page=1, per_page=limit, pages=0)
    
    def update_client(
        self, 
        client_id: str, 
        client_data: ClientUpdate
    ) -> Optional[ClientModel]:
        """
        Update a client.
        
        Args:
            client_id: Client ID
            client_data: Client update data
            
        Returns:
            Updated client or None if failed
        """
        try:
            # Convert to dict and remove None values
            data = {k: v for k, v in client_data.model_dump().items() if v is not None}
            
            if not data:
                # No data to update
                return self.get_client(client_id)
            
            # Update in database
            response = self.client.table("clients").update(data).eq("id", client_id).execute()
            
            if response.data:
                client_dict = response.data[0]
                return ClientModel(**client_dict)
            
            logger.error(f"Failed to update client {client_id}: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error updating client {client_id}: {e}")
            return None
    
    def delete_client(self, client_id: str) -> bool:
        """
        Delete a client (soft delete by setting is_active to False).
        
        Args:
            client_id: Client ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.table("clients").update(
                {"is_active": False}
            ).eq("id", client_id).execute()
            
            return bool(response.data)
            
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {e}")
            return False
    
    # Invoice CRUD operations
    def create_invoice(self, invoice_data: InvoiceCreate) -> Optional[InvoiceModel]:
        """
        Create a new invoice.
        
        Args:
            invoice_data: Invoice creation data
            
        Returns:
            Created invoice or None if failed
        """
        try:
            # Get client info for denormalization
            client = self.get_client(invoice_data.client_id)
            if not client:
                logger.error(f"Client {invoice_data.client_id} not found")
                return None
            
            # Calculate financial fields
            subtotal = sum(item.total for item in invoice_data.items)
            tax_amount = subtotal * invoice_data.tax_rate
            total_amount = subtotal + tax_amount - invoice_data.discount_amount
            
            # Generate invoice number (simple implementation)
            count_response = self.client.table("invoices").select("id", count="exact").execute()
            invoice_number = f"INV-{(count_response.count or 0) + 1:06d}"
            
            # Prepare data with proper datetime serialization
            data = invoice_data.model_dump()
            data.update({
                "invoice_number": invoice_number,
                "client_name": client.name,
                "client_email": client.email,
                "subtotal": subtotal,
                "tax_amount": tax_amount,
                "total_amount": total_amount,
                "items": [item.model_dump() for item in invoice_data.items],
                # Convert datetime objects to ISO format strings
                "issue_date": invoice_data.issue_date.isoformat(),
                "due_date": invoice_data.due_date.isoformat()
            })
            
            # Insert into database
            response = self.client.table("invoices").insert(data).execute()
            
            if response.data:
                invoice_dict = response.data[0]
                return InvoiceModel(**invoice_dict)
            
            logger.error(f"Failed to create invoice: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            return None
    
    def get_invoice(self, invoice_id: str) -> Optional[InvoiceResponse]:
        """
        Get an invoice by ID with computed fields.
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            Invoice with computed fields or None if not found
        """
        try:
            # Get invoice data
            response = self.client.table("invoices").select("*").eq("id", invoice_id).execute()
            
            if not response.data:
                return None
            
            invoice_dict = response.data[0]
            
            # Get payment information
            payments_response = self.client.table("payments").select(
                "amount, status"
            ).eq("invoice_id", invoice_id).execute()
            
            payments = payments_response.data or []
            amount_paid = sum(
                float(payment.get("amount", 0)) 
                for payment in payments 
                if payment.get("status") == "completed"
            )
            
            total_amount = float(invoice_dict.get("total_amount", 0))
            amount_due = max(0, total_amount - amount_paid)
            
            # Determine payment status
            payment_status = PaymentStatus.PENDING
            if amount_paid >= total_amount:
                payment_status = PaymentStatus.COMPLETED
            elif amount_paid > 0:
                payment_status = PaymentStatus.PENDING  # Partially paid
            
            # Create response model
            invoice_dict.update({
                "payment_status": payment_status,
                "amount_paid": amount_paid,
                "amount_due": amount_due
            })
            
            return InvoiceResponse(**invoice_dict)
            
        except Exception as e:
            logger.error(f"Error getting invoice {invoice_id}: {e}")
            return None
    
    def get_invoices(
        self,
        skip: int = 0,
        limit: int = 100,
        client_id: Optional[str] = None,
        status: Optional[InvoiceStatus] = None
    ) -> PaginatedResponse:
        """
        Get paginated list of invoices.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            client_id: Filter by client ID
            status: Filter by invoice status
            
        Returns:
            Paginated response with invoices
        """
        try:
            # Build query
            query = self.client.table("invoices").select("*", count="exact")
            
            if client_id:
                query = query.eq("client_id", client_id)
            
            if status:
                query = query.eq("status", status.value)
            
            # Apply pagination
            query = query.range(skip, skip + limit - 1).order("created_at", desc=True)
            
            response = query.execute()
            
            invoices = [InvoiceModel(**invoice) for invoice in response.data or []]
            total = response.count or 0
            
            return PaginatedResponse(
                items=invoices,
                total=total,
                page=(skip // limit) + 1,
                per_page=limit,
                pages=(total + limit - 1) // limit
            )
            
        except Exception as e:
            logger.error(f"Error getting invoices: {e}")
            return PaginatedResponse(items=[], total=0, page=1, per_page=limit, pages=0)
    
    def update_invoice(
        self,
        invoice_id: str,
        invoice_data: InvoiceUpdate
    ) -> Optional[InvoiceModel]:
        """
        Update an invoice.
        
        Args:
            invoice_id: Invoice ID
            invoice_data: Invoice update data
            
        Returns:
            Updated invoice or None if failed
        """
        try:
            # Convert to dict and remove None values
            data = {k: v for k, v in invoice_data.model_dump().items() if v is not None}
            
            if not data:
                # No data to update
                current = self.get_invoice(invoice_id)
                return InvoiceModel(**current.model_dump()) if current else None
            
            # Recalculate financial fields if items changed
            if "items" in data:
                items = data["items"]
                subtotal = sum(item["total"] for item in items)
                
                # Get current tax rate if not provided
                if "tax_rate" not in data:
                    current_response = self.client.table("invoices").select("tax_rate").eq("id", invoice_id).execute()
                    if current_response.data:
                        data["tax_rate"] = current_response.data[0]["tax_rate"]
                
                tax_rate = data.get("tax_rate", 0)
                discount_amount = data.get("discount_amount", 0)
                
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount - discount_amount
                
                data.update({
                    "subtotal": subtotal,
                    "tax_amount": tax_amount,
                    "total_amount": total_amount
                })
            
            # Update in database
            response = self.client.table("invoices").update(data).eq("id", invoice_id).execute()
            
            if response.data:
                invoice_dict = response.data[0]
                return InvoiceModel(**invoice_dict)
            
            logger.error(f"Failed to update invoice {invoice_id}: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error updating invoice {invoice_id}: {e}")
            return None
    
    def delete_invoice(self, invoice_id: str) -> bool:
        """
        Delete an invoice.
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.table("invoices").delete().eq("id", invoice_id).execute()
            return bool(response.data)
            
        except Exception as e:
            logger.error(f"Error deleting invoice {invoice_id}: {e}")
            return False
    
    # Payment CRUD operations
    def create_payment(self, payment_data: PaymentCreate) -> Optional[PaymentModel]:
        """
        Create a new payment.
        
        Args:
            payment_data: Payment creation data
            
        Returns:
            Created payment or None if failed
        """
        try:
            # Verify invoice exists
            invoice = self.get_invoice(payment_data.invoice_id)
            if not invoice:
                logger.error(f"Invoice {payment_data.invoice_id} not found")
                return None
            
            # Convert Pydantic model to dict with proper datetime serialization
            data = payment_data.model_dump()
            # Convert datetime to ISO format string
            data["payment_date"] = payment_data.payment_date.isoformat()
            
            # Insert into database
            response = self.client.table("payments").insert(data).execute()
            
            if response.data:
                payment_dict = response.data[0]
                
                # Update invoice status if fully paid
                total_paid = self._calculate_total_payments(payment_data.invoice_id)
                if total_paid >= invoice.total_amount:
                    self.update_invoice(
                        payment_data.invoice_id,
                        InvoiceUpdate(status=InvoiceStatus.PAID)
                    )
                
                return PaymentModel(**payment_dict)
            
            logger.error(f"Failed to create payment: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            return None
    
    def get_payment(self, payment_id: str) -> Optional[PaymentModel]:
        """
        Get a payment by ID.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment or None if not found
        """
        try:
            response = self.client.table("payments").select("*").eq("id", payment_id).execute()
            
            if response.data:
                payment_dict = response.data[0]
                return PaymentModel(**payment_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting payment {payment_id}: {e}")
            return None
    
    def get_payments(
        self,
        skip: int = 0,
        limit: int = 100,
        invoice_id: Optional[str] = None,
        status: Optional[PaymentStatus] = None
    ) -> PaginatedResponse:
        """
        Get paginated list of payments.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            invoice_id: Filter by invoice ID
            status: Filter by payment status
            
        Returns:
            Paginated response with payments
        """
        try:
            # Build query
            query = self.client.table("payments").select("*", count="exact")
            
            if invoice_id:
                query = query.eq("invoice_id", invoice_id)
            
            if status:
                query = query.eq("status", status.value)
            
            # Apply pagination
            query = query.range(skip, skip + limit - 1).order("created_at", desc=True)
            
            response = query.execute()
            
            payments = [PaymentModel(**payment) for payment in response.data or []]
            total = response.count or 0
            
            return PaginatedResponse(
                items=payments,
                total=total,
                page=(skip // limit) + 1,
                per_page=limit,
                pages=(total + limit - 1) // limit
            )
            
        except Exception as e:
            logger.error(f"Error getting payments: {e}")
            return PaginatedResponse(items=[], total=0, page=1, per_page=limit, pages=0)
    
    def update_payment(
        self,
        payment_id: str,
        payment_data: PaymentUpdate
    ) -> Optional[PaymentModel]:
        """
        Update a payment.
        
        Args:
            payment_id: Payment ID
            payment_data: Payment update data
            
        Returns:
            Updated payment or None if failed
        """
        try:
            # Convert to dict and remove None values
            data = {k: v for k, v in payment_data.model_dump().items() if v is not None}
            
            if not data:
                # No data to update
                return self.get_payment(payment_id)
            
            # Update in database
            response = self.client.table("payments").update(data).eq("id", payment_id).execute()
            
            if response.data:
                payment_dict = response.data[0]
                return PaymentModel(**payment_dict)
            
            logger.error(f"Failed to update payment {payment_id}: {response}")
            return None
            
        except Exception as e:
            logger.error(f"Error updating payment {payment_id}: {e}")
            return None
    
    def delete_payment(self, payment_id: str) -> bool:
        """
        Delete a payment.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.table("payments").delete().eq("id", payment_id).execute()
            return bool(response.data)
            
        except Exception as e:
            logger.error(f"Error deleting payment {payment_id}: {e}")
            return False
    
    # Helper methods
    def _calculate_total_payments(self, invoice_id: str) -> float:
        """Calculate total completed payments for an invoice."""
        try:
            response = self.client.table("payments").select("amount").eq(
                "invoice_id", invoice_id
            ).eq("status", "completed").execute()
            
            return sum(float(payment.get("amount", 0)) for payment in response.data or [])
            
        except Exception as e:
            logger.error(f"Error calculating total payments for invoice {invoice_id}: {e}")
            return 0.0


# Global CRUD service instance
crud_service: Optional[CRUDService] = None


def get_crud_service() -> CRUDService:
    """
    Get or create a global CRUD service instance.
    
    Returns:
        CRUDService: Configured CRUD service instance
    """
    global crud_service
    
    if crud_service is None:
        crud_service = CRUDService()
        
    return crud_service 