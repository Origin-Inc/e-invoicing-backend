"""Supabase Storage service for E-Invoicing application."""

import os
import mimetypes
from typing import Optional, Dict, Any, List
from pathlib import Path
from supabase import Client
from .supabase_client import get_supabase_client
import logging

logger = logging.getLogger(__name__)

class StorageService:
    """Service class for handling Supabase Storage operations."""
    
    def __init__(self, client: Optional[Client] = None):
        """
        Initialize the Storage Service.
        
        Args:
            client: Optional Supabase client instance. If not provided, 
                   will use the default client.
        """
        self.client = client or get_supabase_client()
        self.buckets = {
            'invoices': 'invoice-documents',
            'receipts': 'receipt-images',
            'templates': 'invoice-templates',
            'exports': 'exported-data'
        }
    
    def create_buckets(self) -> Dict[str, bool]:
        """
        Create all required storage buckets for the application.
        
        Returns:
            Dict[str, bool]: Status of bucket creation for each bucket
        """
        results = {}
        
        for bucket_type, bucket_name in self.buckets.items():
            try:
                # Check if bucket already exists
                existing_buckets = self.client.storage.list_buckets()
                bucket_exists = any(b.name == bucket_name for b in existing_buckets)
                
                if not bucket_exists:
                    # Create bucket with public access for easy development
                    response = self.client.storage.create_bucket(
                        bucket_name,
                        options={"public": True}
                    )
                    results[bucket_name] = True
                    logger.info(f"Created storage bucket: {bucket_name}")
                else:
                    results[bucket_name] = True
                    logger.info(f"Storage bucket already exists: {bucket_name}")
                    
            except Exception as e:
                logger.error(f"Failed to create bucket {bucket_name}: {e}")
                results[bucket_name] = False
                
        return results
    
    def upload_file(
        self,
        bucket_type: str,
        file_path: str,
        file_name: Optional[str] = None,
        folder: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Upload a file to the specified bucket.
        
        Args:
            bucket_type: Type of bucket ('invoices', 'receipts', 'templates', 'exports')
            file_path: Local path to the file to upload
            file_name: Optional custom filename. If not provided, uses original filename
            folder: Optional folder within the bucket
            
        Returns:
            Dict with upload result information or None if failed
        """
        if bucket_type not in self.buckets:
            logger.error(f"Invalid bucket type: {bucket_type}")
            return None
            
        bucket_name = self.buckets[bucket_type]
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
            
        try:
            # Determine filename
            if not file_name:
                file_name = Path(file_path).name
                
            # Create storage path
            storage_path = f"{folder}/{file_name}" if folder else file_name
            
            # Read file content
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Upload file
            response = self.client.storage.from_(bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={
                    "content-type": mime_type,
                    "cache-control": "3600"
                }
            )
            
            if response.path:
                # Get public URL
                public_url = self.client.storage.from_(bucket_name).get_public_url(storage_path)
                
                result = {
                    "success": True,
                    "bucket": bucket_name,
                    "path": storage_path,
                    "size": len(file_content),
                    "mime_type": mime_type,
                    "public_url": public_url
                }
                logger.info(f"Successfully uploaded file: {storage_path}")
                return result
            else:
                logger.error(f"Upload failed: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            return None
    
    def download_file(
        self,
        bucket_type: str,
        file_path: str,
        local_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Download a file from storage.
        
        Args:
            bucket_type: Type of bucket
            file_path: Path to file in storage
            local_path: Optional local path to save. If not provided, returns file content
            
        Returns:
            Local file path if saved, or None if failed
        """
        if bucket_type not in self.buckets:
            logger.error(f"Invalid bucket type: {bucket_type}")
            return None
            
        bucket_name = self.buckets[bucket_type]
        
        try:
            # Download file
            response = self.client.storage.from_(bucket_name).download(file_path)
            
            if local_path:
                # Save to local file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(response)
                logger.info(f"Downloaded file to: {local_path}")
                return local_path
            else:
                # Return content
                return response
                
        except Exception as e:
            logger.error(f"Error downloading file {file_path}: {e}")
            return None
    
    def delete_file(self, bucket_type: str, file_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            bucket_type: Type of bucket
            file_path: Path to file in storage
            
        Returns:
            True if successful, False otherwise
        """
        if bucket_type not in self.buckets:
            logger.error(f"Invalid bucket type: {bucket_type}")
            return False
            
        bucket_name = self.buckets[bucket_type]
        
        try:
            response = self.client.storage.from_(bucket_name).remove([file_path])
            if response:
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def list_files(
        self,
        bucket_type: str,
        folder: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List files in a bucket or folder.
        
        Args:
            bucket_type: Type of bucket
            folder: Optional folder to list
            limit: Maximum number of files to return
            
        Returns:
            List of file information dictionaries
        """
        if bucket_type not in self.buckets:
            logger.error(f"Invalid bucket type: {bucket_type}")
            return []
            
        bucket_name = self.buckets[bucket_type]
        
        try:
            response = self.client.storage.from_(bucket_name).list(
                path=folder or "",
                options={"limit": limit}
            )
            
            files = []
            for item in response:
                file_info = {
                    "name": item.get("name"),
                    "size": item.get("metadata", {}).get("size", 0),
                    "created_at": item.get("created_at"),
                    "updated_at": item.get("updated_at"),
                    "public_url": self.client.storage.from_(bucket_name).get_public_url(
                        f"{folder}/{item.get('name')}" if folder else item.get("name")
                    )
                }
                files.append(file_info)
            
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in {bucket_name}: {e}")
            return []
    
    def get_file_url(self, bucket_type: str, file_path: str) -> Optional[str]:
        """
        Get the public URL for a file.
        
        Args:
            bucket_type: Type of bucket
            file_path: Path to file in storage
            
        Returns:
            Public URL string or None if failed
        """
        if bucket_type not in self.buckets:
            logger.error(f"Invalid bucket type: {bucket_type}")
            return None
            
        bucket_name = self.buckets[bucket_type]
        
        try:
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_path)
            return public_url
        except Exception as e:
            logger.error(f"Error getting file URL for {file_path}: {e}")
            return None


# Global storage service instance
storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """
    Get or create a global storage service instance.
    
    Returns:
        StorageService: Configured storage service instance
    """
    global storage_service
    
    if storage_service is None:
        storage_service = StorageService()
        
    return storage_service


def initialize_storage() -> Dict[str, bool]:
    """
    Initialize storage by creating all required buckets.
    
    Returns:
        Dict[str, bool]: Status of bucket creation
    """
    service = get_storage_service()
    return service.create_buckets() 