-- Create main application tables for E-Invoicing
-- This migration creates the core tables: clients, invoices, and payments

-- Create clients table
CREATE TABLE IF NOT EXISTS clients (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    phone varchar(20),
    address text,
    city varchar(100),
    state varchar(100),
    zip_code varchar(20),
    country varchar(100),
    tax_id varchar(50),
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number varchar(50) NOT NULL UNIQUE,
    client_id uuid NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    client_name varchar(255),
    client_email varchar(255),
    issue_date timestamp with time zone NOT NULL,
    due_date timestamp with time zone NOT NULL,
    status varchar(20) DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')),
    subtotal decimal(10,2) NOT NULL CHECK (subtotal >= 0),
    tax_rate decimal(5,4) DEFAULT 0.0 CHECK (tax_rate >= 0 AND tax_rate <= 1),
    tax_amount decimal(10,2) NOT NULL CHECK (tax_amount >= 0),
    discount_amount decimal(10,2) DEFAULT 0.0 CHECK (discount_amount >= 0),
    total_amount decimal(10,2) NOT NULL CHECK (total_amount >= 0),
    items jsonb NOT NULL,
    notes text,
    terms text,
    pdf_url text,
    attachment_urls jsonb DEFAULT '[]',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id uuid NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    amount decimal(10,2) NOT NULL CHECK (amount > 0),
    payment_date timestamp with time zone NOT NULL,
    payment_method varchar(50) NOT NULL,
    status varchar(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    transaction_id varchar(100),
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_clients_active ON clients(is_active);
CREATE INDEX IF NOT EXISTS idx_invoices_client_id ON invoices(client_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date);
CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_payments_invoice_id ON payments(invoice_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(payment_date);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) for all tables
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Create permissive policies for development (tighten for production)
CREATE POLICY "Allow all operations on clients for development" ON clients
FOR ALL USING (true);

CREATE POLICY "Allow all operations on invoices for development" ON invoices
FOR ALL USING (true);

CREATE POLICY "Allow all operations on payments for development" ON payments
FOR ALL USING (true); 