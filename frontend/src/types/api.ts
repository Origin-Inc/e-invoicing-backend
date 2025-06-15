// API Configuration
export interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

// Generic API Response
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
  timestamp: string;
}

// Generic Error Response
export interface ApiError {
  message: string;
  status: number;
  details?: any;
  timestamp?: string;
}

// Paginated Response
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  hasNext: boolean;
  hasPrev: boolean;
}

// Request Types for Client
export interface CreateClientRequest {
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
}

export interface UpdateClientRequest extends Partial<CreateClientRequest> {}

// Request Types for Invoice
export interface CreateInvoiceRequest {
  clientId: string;
  dueDate: string;
  items: Array<{
    description: string;
    quantity: number;
    rate: number;
    amount: number;
  }>;
  subtotal: number;
  taxRate?: number;
  taxAmount?: number;
  discountRate?: number;
  discountAmount?: number;
  totalAmount: number;
  notes?: string;
  terms?: string;
}

export interface UpdateInvoiceRequest extends Partial<CreateInvoiceRequest> {
  status?: 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled';
}

// Request Types for Payment
export interface CreatePaymentRequest {
  invoiceId: string;
  amount: number;
  paymentMethod: string;
  paymentDate?: string;
  notes?: string;
  reference?: string;
}

export interface UpdatePaymentRequest extends Partial<CreatePaymentRequest> {
  status?: 'pending' | 'completed' | 'failed' | 'refunded';
}

// Health Check Response
export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    database: 'healthy' | 'unhealthy';
    supabase: 'healthy' | 'unhealthy';
    redis?: 'healthy' | 'unhealthy';
  };
  version: string;
}

export interface ListParams {
  page?: number;
  limit?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    database: boolean;
    supabase: boolean;
    redis?: boolean;
  };
  version: string;
} 