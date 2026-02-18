import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import mimetypes
import os

from app.core.config import settings


class B2StorageService:
    """
    Service for interacting with Backblaze B2 cloud storage
    Handles file uploads, downloads, and management
    """
    
    def __init__(self):
        """Initialize B2 client with settings from environment"""
        print("\n" + "=" * 50)
        print("🔧 Initializing B2 Storage Service")
        print("=" * 50)
        
        # Load settings
        self.endpoint = settings.B2_ENDPOINT
        self.key_id = settings.B2_KEY_ID
        self.app_key = settings.B2_APP_KEY
        self.bucket_name = settings.B2_BUCKET_NAME
        self.bucket_id = settings.B2_BUCKET_ID
        self.region = settings.B2_REGION
        self.max_file_size = settings.B2_MAX_FILE_SIZE_MB
        self.allowed_types = settings.B2_ALLOWED_FILE_TYPES
        
        # Print settings for debugging
        print(f"B2_ENDPOINT: {self.endpoint}")
        print(f"B2_KEY_ID: {self.key_id}")
        print(f"B2_APP_KEY: {'*' * 8 if self.app_key else 'None'}")
        print(f"B2_BUCKET_NAME: {self.bucket_name}")
        print(f"B2_BUCKET_ID: {self.bucket_id}")
        print(f"B2_REGION: {self.region}")
        print(f"Max file size: {self.max_file_size} bytes ({self.max_file_size/1024/1024:.0f}MB)")
        print(f"Allowed types: {len(self.allowed_types)} types configured")
        
        # Validate required settings
        missing = []
        if not self.key_id:
            missing.append("B2_KEY_ID")
        if not self.app_key:
            missing.append("B2_APP_KEY")
        if not self.bucket_name:
            missing.append("B2_BUCKET_NAME")
        
        if missing:
            error_msg = f"B2 credentials not properly configured. Missing: {', '.join(missing)}. Check your .env file."
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        print("✅ All required B2 credentials present")
        
        # Initialize S3-compatible client
        try:
            self.client = boto3.client(
                's3',
                endpoint_url=f'https://{self.endpoint}',
                aws_access_key_id=self.key_id,
                aws_secret_access_key=self.app_key,
                config=Config(
                    signature_version='s3v4',
                    s3={'addressing_style': 'path'}
                )
            )
            print("✅ B2 client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize B2 client: {e}")
            raise
        
        # Verify connection on initialization
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to B2 by listing buckets"""
        try:
            response = self.client.list_buckets()
            print(f"✅ Connected to B2 successfully")
            print(f"   Account ID: {response.get('Owner', {}).get('ID', 'Unknown')}")
            print(f"   Buckets found: {len(response.get('Buckets', []))}")
            return True
        except Exception as e:
            print(f"⚠️  B2 Connection warning: {e}")
            return False
    
    def validate_file(self, file_content: bytes, content_type: str, filename: str) -> Dict[str, Any]:
        """
        Validate file size and type before upload
        """
        errors = []
        
        # Check file size
        file_size = len(file_content)
        if file_size > self.max_file_size:
            errors.append(f"File size ({file_size} bytes) exceeds maximum allowed ({self.max_file_size} bytes)")
        
        # Check file type
        if content_type not in self.allowed_types:
            # Try to guess from extension
            guessed_type = mimetypes.guess_type(filename)[0]
            if guessed_type not in self.allowed_types:
                errors.append(f"File type '{content_type}' not allowed. Allowed types: {', '.join(self.allowed_types)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "file_size": file_size,
            "file_type": content_type
        }
    
    def generate_unique_filename(self, employee_id: int, original_filename: str) -> str:
        """
        Generate a unique filename for B2 storage
        Format: emp_{employee_id}_{timestamp}_{uuid}_{original_filename}
        """
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = str(uuid.uuid4())[:8]
        
        # Sanitize original filename (remove special chars, spaces)
        safe_filename = "".join(c for c in original_filename if c.isalnum() or c in '._-').strip()
        if not safe_filename:
            safe_filename = "document"
        
        return f"emp_{employee_id}_{timestamp}_{unique_id}_{safe_filename}"
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        employee_id: int,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to Backblaze B2
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            content_type: MIME type of the file
            employee_id: ID of the employee uploading
            metadata: Additional metadata to store with the file
            
        Returns:
            Dict with file metadata from B2
        """
        try:
            # Validate file first
            validation = self.validate_file(file_content, content_type, filename)
            if not validation["valid"]:
                raise ValueError(f"File validation failed: {', '.join(validation['errors'])}")
            
            # Generate unique filename for storage
            unique_filename = self.generate_unique_filename(employee_id, filename)
            
            # Prepare metadata
            file_metadata = {
                'employee_id': str(employee_id),
                'original_filename': filename,
                'upload_date': datetime.utcnow().isoformat(),
                'content_type': content_type,
                **(metadata or {})
            }
            
            # Upload to B2
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ContentType=content_type,
                Metadata=file_metadata
            )
            
            # Get file info to return
            file_info = self.get_file_info(unique_filename)
            
            return {
                "success": True,
                "fileId": unique_filename,
                "fileName": unique_filename,
                "originalFileName": filename,
                "bucketId": self.bucket_id,
                "bucketName": self.bucket_name,
                "contentLength": len(file_content),
                "contentType": content_type,
                "uploadTimestamp": int(datetime.utcnow().timestamp() * 1000),
                "fileInfo": file_metadata,
                "etag": file_info.get("ETag", "").strip('"') if file_info else "",
                "storageClass": "STANDARD"
            }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            raise Exception(f"B2 upload failed ({error_code}): {error_message}")
        
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")
    
    def get_file_info(self, file_name: str) -> Dict[str, Any]:
        """
        Get metadata about a file from B2
        """
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise Exception(f"File not found: {file_name}")
            raise
    
    def get_download_url(
        self,
        file_name: str,
        expires_in: int = 3600,
        response_content_disposition: Optional[str] = None
    ) -> str:
        """
        Generate a presigned URL for file download
        
        Args:
            file_name: Name of the file in B2
            expires_in: URL expiration time in seconds (default: 1 hour)
            response_content_disposition: Force download with custom filename
            
        Returns:
            Presigned URL for temporary access
        """
        try:
            params = {
                'Bucket': self.bucket_name,
                'Key': file_name
            }
            
            if response_content_disposition:
                params['ResponseContentDisposition'] = f'attachment; filename="{response_content_disposition}"'
            
            url = self.client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate download URL: {str(e)}")
    
    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from B2
        
        Returns:
            True if successful
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            raise Exception(f"B2 delete failed ({error_code}): {str(e)}")
    
    def list_files(
        self,
        prefix: Optional[str] = None,
        max_keys: int = 100,
        employee_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List files in the bucket
        
        Args:
            prefix: Optional prefix to filter files
            max_keys: Maximum number of files to return
            employee_id: Optional employee ID to filter files
            
        Returns:
            List of file metadata
        """
        try:
            params = {
                'Bucket': self.bucket_name,
                'MaxKeys': max_keys
            }
            
            if prefix:
                params['Prefix'] = prefix
            
            response = self.client.list_objects_v2(**params)
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    file_info = {
                        'fileName': obj['Key'],
                        'size': obj['Size'],
                        'lastModified': obj['LastModified'].isoformat() if obj.get('LastModified') else None,
                        'etag': obj['ETag'].strip('"') if obj.get('ETag') else None
                    }
                    
                    # If employee_id provided, filter by it
                    if employee_id:
                        if obj['Key'].startswith(f"emp_{employee_id}_"):
                            files.append(file_info)
                    else:
                        files.append(file_info)
            
            return files
            
        except Exception as e:
            raise Exception(f"Failed to list files: {str(e)}")
    
    def file_exists(self, file_name: str) -> bool:
        """
        Check if a file exists in B2
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError:
            return False
    
    def copy_file(self, source_file_name: str, destination_file_name: str) -> bool:
        """
        Copy a file within B2
        """
        try:
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': source_file_name
            }
            
            self.client.copy_object(
                CopySource=copy_source,
                Bucket=self.bucket_name,
                Key=destination_file_name
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to copy file: {str(e)}")
    
    def get_file_size(self, file_name: str) -> int:
        """
        Get the size of a file in bytes
        """
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return response['ContentLength']
        except Exception as e:
            raise Exception(f"Failed to get file size: {str(e)}")
    
    def get_bucket_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the bucket
        """
        try:
            files = self.list_files(max_keys=1000)
            total_size = sum(f['size'] for f in files)
            
            return {
                "bucketName": self.bucket_name,
                "bucketId": self.bucket_id,
                "totalFiles": len(files),
                "totalSize": total_size,
                "totalSizeMB": round(total_size / (1024 * 1024), 2),
                "endpoint": self.endpoint
            }
        except Exception as e:
            raise Exception(f"Failed to get bucket stats: {str(e)}")
    
    async def upload_file_from_path(
        self,
        file_path: str,
        employee_id: int,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file from local filesystem
        """
        try:
            filename = os.path.basename(file_path)
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            return await self.upload_file(
                file_content=file_content,
                filename=filename,
                content_type=content_type,
                employee_id=employee_id,
                metadata=metadata
            )
        except Exception as e:
            raise Exception(f"Failed to upload file from path: {str(e)}")


# Create a singleton instance
try:
    print("\n🚀 Creating B2 Storage Service instance...")
    b2_storage = B2StorageService()
    print("✅ B2 Storage Service initialized successfully!\n")
except Exception as e:
    print(f"❌ Failed to create B2 Storage Service: {e}")
    b2_storage = None