// Payment entity types
export interface Payment {
  id: string;
  invoiceId: string;
  amount: number;
  paymentDate: string;
  paymentMethod: string;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  reference?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface PaymentWithInvoice extends Payment {
  invoice: {
    id: string;
    invoiceNumber: string;
    clientId: string;
    totalAmount: number;
    client: {
      id: string;
      name: string;
    };
  };
} 