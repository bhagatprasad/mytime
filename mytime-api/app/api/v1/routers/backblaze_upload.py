from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import json
from datetime import datetime

from app.core.database import get_db
from app.services.b2_storage_service import b2_storage
from app.services.employee_document_service import EmployeeDocumentService
from app.schemas.employee_document_schemas import EmployeeDocumentResponse, EmployeeDocumentDeleteResponse
from app.core.config import settings

router = APIRouter()


@router.post("/upload-document/{employee_id}")
async def upload_employee_document(
    employee_id: int,
    file: UploadFile = File(...),
    document_type: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a document to Backblaze B2 and save metadata to database
    """
    try:
        # Check if B2 storage is enabled
        if not settings.ENABLE_B2_STORAGE:
            raise HTTPException(status_code=503, detail="B2 storage is currently disabled")
        
        # Read file content
        file_content = await file.read()
        
        # Step 1: Upload to Backblaze B2
        b2_response = await b2_storage.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type or 'application/octet-stream',
            employee_id=employee_id,
            metadata={
                'document_type': document_type,
                'description': description or '',
                'uploaded_by': 'employee'
            }
        )
        
        # Step 2: Prepare document data for database
        document_data = {
            "EmployeeId": employee_id,
            "DocumentType": document_type,
            "FileId": b2_response["fileId"],
            "FileName": b2_response["fileName"],
            "BucketId": b2_response["bucketId"],
            "ContentLength": b2_response["contentLength"],
            "ContentType": b2_response["contentType"],
            "FileInfo": json.dumps({
                "description": description,
                "original_filename": file.filename,
                "b2_metadata": b2_response.get("fileInfo", {})
            }),
            "UploadTimestamp": datetime.utcnow().isoformat(),
            "IsActive": True
        }
        
        # Step 3: Save to database using your existing service
        db_response = EmployeeDocumentService.insert_or_update_employee_document(db, document_data)
        
        if not db_response["success"]:
            # If database save fails, delete from B2 to keep consistency
            try:
                b2_storage.delete_file(b2_response["fileName"])
            except:
                pass  # Log this in production
            raise HTTPException(status_code=500, detail=db_response["message"])
        
        # Step 4: Generate download URL
        download_url = b2_storage.get_download_url(b2_response["fileName"])
        
        # Step 5: Return combined response
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "b2_data": b2_response,
            "db_data": db_response["document"],
            "downloadUrl": download_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/download-url/{file_name}")
async def get_download_url(
    file_name: str,
    expires_in: int = Query(3600, ge=60, le=86400),  # 1 min to 24 hours
    filename: Optional[str] = None  # Custom filename for download
):
    """
    Get a temporary download URL for a file
    """
    try:
        # Verify file exists
        if not b2_storage.file_exists(file_name):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Generate URL
        url = b2_storage.get_download_url(
            file_name, 
            expires_in=expires_in,
            response_content_disposition=filename
        )
        
        return {
            "url": url,
            "expiresIn": expires_in,
            "expiresAt": datetime.utcnow().timestamp() + expires_in,
            "fileName": file_name,
            "downloadFilename": filename or file_name
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate URL: {str(e)}")


@router.delete("/delete-file/{file_name}/{employee_document_id}")
async def delete_b2_file(
    file_name: str,
    employee_document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete file from B2 and database
    """
    try:
        # Step 1: Delete from B2
        b2_storage.delete_file(file_name)
        
        # Step 2: Delete from database using your existing service
        db_response = EmployeeDocumentService.delete_employee_document(db, employee_document_id)
        
        if not db_response["success"]:
            raise HTTPException(status_code=404, detail=db_response["message"])
        
        return {
            "success": True,
            "message": "File deleted successfully from B2 and database"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.get("/file-info/{file_name}")
async def get_file_info(file_name: str):
    """
    Get metadata about a file in B2
    """
    try:
        # Verify file exists
        if not b2_storage.file_exists(file_name):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file info
        file_info = b2_storage.get_file_info(file_name)
        
        # Parse metadata
        metadata = {}
        if 'Metadata' in file_info:
            metadata = {k: v for k, v in file_info['Metadata'].items()}
        
        return {
            "fileName": file_name,
            "size": file_info.get('ContentLength', 0),
            "contentType": file_info.get('ContentType', ''),
            "lastModified": file_info.get('LastModified', '').isoformat() if file_info.get('LastModified') else None,
            "etag": file_info.get('ETag', '').strip('"'),
            "metadata": metadata,
            "storageClass": file_info.get('StorageClass', 'STANDARD')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")


@router.get("/bucket-stats")
async def get_bucket_stats():
    """
    Get statistics about the bucket
    """
    try:
        stats = b2_storage.get_bucket_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get bucket stats: {str(e)}")


@router.get("/list-files")
async def list_files(
    prefix: Optional[str] = None,
    employee_id: Optional[int] = None,
    limit: int = Query(100, le=1000)
):
    """
    List files in the bucket
    """
    try:
        files = b2_storage.list_files(
            prefix=prefix,
            max_keys=limit,
            employee_id=employee_id
        )
        return {
            "total": len(files),
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")