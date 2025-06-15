// Invoice entity types
export interface Invoice {
  id: string;
  client_id: string;
  invoice_number: string;
  amount: number;
  tax_amount?: number;
  discount_amount?: number;
  status: 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled';
  due_date: string;
  issue_date: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateInvoiceRequest {
  client_id: string;
  amount: number;
  tax_amount?: number;
  discount_amount?: number;
  status?: 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled';
  due_date: string;
  issue_date: string;
  description?: string;
}

export interface UpdateInvoiceRequest extends Partial<CreateInvoiceRequest> {}

export interface InvoiceWithClient extends Invoice {
  client: {
    id: string;
    name: string;
    email: string;
  };
}

export interface InvoiceStats {
  total_amount: number;
  paid_amount: number;
  pending_amount: number;
  overdue_amount: number;
  count: number;
} 