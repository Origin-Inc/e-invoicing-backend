-- Create storage buckets for E-Invoicing application
-- This migration sets up the required storage buckets with appropriate permissions

-- Create buckets
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES 
  ('invoice-documents', 'invoice-documents', true, 52428800, ARRAY['application/pdf', 'image/jpeg', 'image/png']),
  ('receipt-images', 'receipt-images', true, 10485760, ARRAY['image/jpeg', 'image/png', 'image/webp']),
  ('invoice-templates', 'invoice-templates', true, 5242880, ARRAY['application/pdf', 'text/html', 'application/json']),
  ('exported-data', 'exported-data', true, 104857600, ARRAY['application/json', 'text/csv', 'application/zip'])
ON CONFLICT (id) DO NOTHING;

-- Create storage policies for public access during development
-- Note: These are permissive policies for development. Tighten for production.

-- Policy for invoice-documents bucket
CREATE POLICY "Allow all operations on invoice-documents for development" ON storage.objects
FOR ALL USING (bucket_id = 'invoice-documents');

-- Policy for receipt-images bucket  
CREATE POLICY "Allow all operations on receipt-images for development" ON storage.objects
FOR ALL USING (bucket_id = 'receipt-images');

-- Policy for invoice-templates bucket
CREATE POLICY "Allow all operations on invoice-templates for development" ON storage.objects
FOR ALL USING (bucket_id = 'invoice-templates');

-- Policy for exported-data bucket
CREATE POLICY "Allow all operations on exported-data for development" ON storage.objects
FOR ALL USING (bucket_id = 'exported-data'); 