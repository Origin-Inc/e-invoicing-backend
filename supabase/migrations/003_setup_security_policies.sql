-- 003_setup_security_policies.sql
-- Security policies for E-Invoicing application
-- Development-friendly policies with proper foundation for production

-- Enable RLS on all tables
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- CLIENT TABLE POLICIES
-- ============================================================

-- Allow all operations for authenticated users (development)
CREATE POLICY "clients_authenticated_all" 
ON public.clients
FOR ALL 
TO authenticated
USING (true)
WITH CHECK (true);

-- Allow service role full access (for API operations)
CREATE POLICY "clients_service_role_all" 
ON public.clients
FOR ALL 
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================================
-- INVOICE TABLE POLICIES
-- ============================================================

-- Allow all operations for authenticated users (development)
CREATE POLICY "invoices_authenticated_all" 
ON public.invoices
FOR ALL 
TO authenticated
USING (true)
WITH CHECK (true);

-- Allow service role full access (for API operations)
CREATE POLICY "invoices_service_role_all" 
ON public.invoices
FOR ALL 
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================================
-- PAYMENT TABLE POLICIES
-- ============================================================

-- Allow all operations for authenticated users (development)
CREATE POLICY "payments_authenticated_all" 
ON public.payments
FOR ALL 
TO authenticated
USING (true)
WITH CHECK (true);

-- Allow service role full access (for API operations)
CREATE POLICY "payments_service_role_all" 
ON public.payments
FOR ALL 
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================================
-- STORAGE POLICIES
-- ============================================================

-- Update storage bucket policies to allow service role access
-- This fixes the bucket creation issues we were seeing

-- Invoice documents bucket
INSERT INTO storage.policies (id, bucket_id, policy_name, type, command, target_role, created_at)
VALUES (
    gen_random_uuid(),
    'invoice-documents',
    'Allow service role all operations',
    'storage',
    'ALL',
    'service_role',
    now()
) ON CONFLICT DO NOTHING;

-- Receipt images bucket
INSERT INTO storage.policies (id, bucket_id, policy_name, type, command, target_role, created_at)
VALUES (
    gen_random_uuid(),
    'receipt-images',
    'Allow service role all operations',
    'storage',
    'ALL',
    'service_role',
    now()
) ON CONFLICT DO NOTHING;

-- Invoice templates bucket
INSERT INTO storage.policies (id, bucket_id, policy_name, type, command, target_role, created_at)
VALUES (
    gen_random_uuid(),
    'invoice-templates',
    'Allow service role all operations',
    'storage',
    'ALL',
    'service_role',
    now()
) ON CONFLICT DO NOTHING;

-- Exported data bucket
INSERT INTO storage.policies (id, bucket_id, policy_name, type, command, target_role, created_at)
VALUES (
    gen_random_uuid(),
    'exported-data',
    'Allow service role all operations',
    'storage',
    'ALL',
    'service_role',
    now()
) ON CONFLICT DO NOTHING;

-- ============================================================
-- SECURITY FUNCTIONS
-- ============================================================

-- Function to check if user owns a client record (for future use)
CREATE OR REPLACE FUNCTION auth.user_owns_client(client_id uuid)
RETURNS boolean AS $$
BEGIN
  -- For development, always return true
  -- In production, this would check ownership
  RETURN true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check if user can access invoice (for future use)
CREATE OR REPLACE FUNCTION auth.user_can_access_invoice(invoice_id uuid)
RETURNS boolean AS $$
BEGIN
  -- For development, always return true
  -- In production, this would check via client ownership
  RETURN true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================
-- GRANTS AND PERMISSIONS
-- ============================================================

-- Grant usage on the auth schema to authenticated users
GRANT USAGE ON SCHEMA auth TO authenticated;
GRANT EXECUTE ON FUNCTION auth.user_owns_client(uuid) TO authenticated;
GRANT EXECUTE ON FUNCTION auth.user_can_access_invoice(uuid) TO authenticated;

-- Grant necessary permissions for API operations
GRANT ALL ON public.clients TO service_role;
GRANT ALL ON public.invoices TO service_role;
GRANT ALL ON public.payments TO service_role;

-- Grant sequence permissions
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================================
-- AUDIT TRAIL SETUP (for future enhancement)
-- ============================================================

-- Create audit log table (disabled for development)
-- CREATE TABLE IF NOT EXISTS public.audit_log (
--     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
--     table_name text NOT NULL,
--     operation text NOT NULL,
--     old_data jsonb,
--     new_data jsonb,
--     user_id uuid REFERENCES auth.users(id),
--     created_at timestamptz DEFAULT now()
-- );

-- Comments for documentation
COMMENT ON POLICY "clients_authenticated_all" ON public.clients 
IS 'Development policy: Allow all operations for authenticated users';

COMMENT ON POLICY "invoices_authenticated_all" ON public.invoices 
IS 'Development policy: Allow all operations for authenticated users';

COMMENT ON POLICY "payments_authenticated_all" ON public.payments 
IS 'Development policy: Allow all operations for authenticated users';

-- Migration complete
SELECT 'Security policies configured for development environment' as status; 