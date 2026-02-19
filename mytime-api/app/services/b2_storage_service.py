import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import mimetypes

from app.core.config import settings


class B2StorageService:
    def __init__(self):
        self.key_id = settings.B2_KEY_ID
        self.app_key = settings.B2_APP_KEY
        self.bucket_name = settings.B2_BUCKET_NAME
        self.bucket_id = settings.B2_BUCKET_ID
        self.region = settings.B2_REGION
        self.max_file_size = settings.B2_MAX_FILE_SIZE_MB
        self.allowed_types = settings.B2_ALLOWED_FILE_TYPES

        # FIX: Strip any accidental https:// prefix from the endpoint setting
        # so we don't end up with https://https://...
        raw_endpoint = settings.B2_ENDPOINT
        if raw_endpoint.startswith("https://"):
            raw_endpoint = raw_endpoint[len("https://"):]
        elif raw_endpoint.startswith("http://"):
            raw_endpoint = raw_endpoint[len("http://"):]
        self.endpoint = raw_endpoint.strip()

        # FIX: Strip whitespace/invisible chars from credentials
        self.key_id = self.key_id.strip() if self.key_id else self.key_id
        self.app_key = self.app_key.strip() if self.app_key else self.app_key
        self.bucket_name = self.bucket_name.strip() if self.bucket_name else self.bucket_name

        missing = []
        if not self.key_id:
            missing.append("B2_KEY_ID")
        if not self.app_key:
            missing.append("B2_APP_KEY")
        if not self.bucket_name:
            missing.append("B2_BUCKET_NAME")
        if not self.endpoint:
            missing.append("B2_ENDPOINT")

        if missing:
            raise ValueError(f"B2 credentials not properly configured. Missing: {', '.join(missing)}")

        # FIX: Build the region name correctly for B2.
        # B2 region strings look like "us-west-004" — extract just that from the endpoint
        # e.g. "s3.us-west-004.backblazeb2.com" → "us-west-004"
        if not self.region:
            parts = self.endpoint.split(".")
            # endpoint format: s3.<region>.backblazeb2.com
            self.region = parts[1] if len(parts) >= 3 else "us-west-004"

        try:
            self.client = boto3.client(
                "s3",
                endpoint_url=f"https://{self.endpoint}",
                aws_access_key_id=self.key_id,
                aws_secret_access_key=self.app_key,
                region_name=self.region,  # FIX: pass region_name explicitly
                config=Config(
                    signature_version="s3v4",
                    s3={"addressing_style": "path"},
                ),
            )
        except Exception as e:
            raise Exception(f"Failed to initialize B2 client: {e}")

        self._test_connection()

    def _test_connection(self) -> bool:
        try:
            self.client.list_buckets()
            return True
        except Exception as e:
            print(f"B2 Connection warning: {e}")
            return False

    def validate_file(self, file_content: bytes, content_type: str, filename: str) -> Dict[str, Any]:
        errors = []

        file_size = len(file_content)
        if file_size > self.max_file_size:
            errors.append(
                f"File size ({file_size} bytes) exceeds maximum allowed ({self.max_file_size} bytes)"
            )

        if content_type not in self.allowed_types:
            guessed_type = mimetypes.guess_type(filename)[0]
            if guessed_type not in self.allowed_types:
                errors.append(
                    f"File type '{content_type}' not allowed. "
                    f"Allowed types: {', '.join(self.allowed_types)}"
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "file_size": file_size,
            "file_type": content_type,
        }

    def generate_unique_filename(self, original_filename: str) -> str:
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = str(uuid.uuid4())[:8]

        safe_filename = "".join(
            c for c in original_filename if c.isalnum() or c in "._-"
        ).strip()
        if not safe_filename:
            safe_filename = "document"

        return f"file_{timestamp}_{unique_id}_{safe_filename}"

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
    ) -> Dict[str, Any]:
        try:
            validation = self.validate_file(file_content, content_type, filename)
            if not validation["valid"]:
                raise ValueError(
                    f"File validation failed: {', '.join(validation['errors'])}"
                )

            unique_filename = self.generate_unique_filename(filename)

            file_metadata = {
                "original_filename": filename,
                "upload_date": datetime.utcnow().isoformat(),
                "content_type": content_type,
            }

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ContentType=content_type,
                Metadata=file_metadata,
            )

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
                "storageClass": "STANDARD",
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            raise Exception(f"B2 upload failed ({error_code}): {error_message}")
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_id,
            )
            return response
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise Exception(f"File not found: {file_id}")
            raise

    def get_download_url(
        self,
        file_id: str,
        expires_in: int = 3600,
        response_content_disposition: Optional[str] = None,
    ) -> str:
        try:
            params: Dict[str, Any] = {
                "Bucket": self.bucket_name,
                "Key": file_id,
            }

            if response_content_disposition:
                params["ResponseContentDisposition"] = (
                    f'attachment; filename="{response_content_disposition}"'
                )

            url = self.client.generate_presigned_url(
                "get_object",
                Params=params,
                ExpiresIn=expires_in,
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate download URL: {str(e)}")

    def delete_file(self, file_id: str) -> bool:
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_id,
            )
            return True
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            raise Exception(f"B2 delete failed ({error_code}): {str(e)}")

    def file_exists(self, file_id: str) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_id,
            )
            return True
        except ClientError:
            return False


try:
    b2_storage = B2StorageService()
except Exception as e:
    print(f"Failed to create B2 Storage Service: {e}")
    b2_storage = None