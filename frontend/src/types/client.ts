// Client entity types
export interface Client {
  id: string;
  name: string;
  email: string;
  phone?: string;
  address?: {
    street?: string;
    city?: string;
    state?: string;
    postalCode?: string;
    country?: string;
  };
  company?: string;
  website?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ClientResponse extends Client {
  // Additional response-only fields if needed
  invoiceCount?: number;
  totalAmount?: number;
  lastInvoiceDate?: string;
} 