from fastapi import APIRouter, HTTPException, File, UploadFile, Query
from typing import Optional
from datetime import datetime, timezone

from app.services.b2_storage_service import b2_storage

router = APIRouter()


def _check_storage():
    """Raise a 503 early if the B2 client failed to initialize."""
    if b2_storage is None:
        raise HTTPException(
            status_code=503,
            detail="Storage service is unavailable. Check B2 configuration.",
        )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    _check_storage()
    try:
        file_content = await file.read()

        # FIX: guard against empty uploads
        if not file_content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        b2_response = await b2_storage.upload_file(
            file_content=file_content,
            filename=file.filename or "upload",
            content_type=file.content_type or "application/octet-stream",
        )

        download_url = b2_storage.get_download_url(b2_response["fileId"])

        return {
            "success": True,
            "fileId": b2_response["fileId"],
            "fileName": file.filename,
            "storedFileName": b2_response["fileName"],
            "contentType": b2_response["contentType"],
            "contentLength": b2_response["contentLength"],
            "uploadTimestamp": b2_response["uploadTimestamp"],
            "downloadUrl": download_url,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/download-url/{file_id}")
async def get_download_url(
    file_id: str,
    expires_in: int = Query(3600, ge=60, le=86400),
    filename: Optional[str] = None,
):
    _check_storage()
    try:
        if not b2_storage.file_exists(file_id):
            raise HTTPException(status_code=404, detail="File not found")

        url = b2_storage.get_download_url(
            file_id,
            expires_in=expires_in,
            response_content_disposition=filename,
        )

        # FIX: use timezone-aware UTC time
        expires_at = datetime.now(tz=timezone.utc).timestamp() + expires_in

        return {
            "success": True,
            "url": url,
            "expiresIn": expires_in,
            "expiresAt": expires_at,
            "fileId": file_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate URL: {str(e)}")


@router.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    _check_storage()
    try:
        if not b2_storage.file_exists(file_id):
            raise HTTPException(status_code=404, detail="File not found")

        b2_storage.delete_file(file_id)

        return {
            "success": True,
            "message": "File deleted successfully",
            "fileId": file_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.get("/info/{file_id}")
async def get_file_info(file_id: str):
    _check_storage()
    try:
        if not b2_storage.file_exists(file_id):
            raise HTTPException(status_code=404, detail="File not found")

        file_info = b2_storage.get_file_info(file_id)

        metadata = {}
        if "Metadata" in file_info:
            metadata = dict(file_info["Metadata"])

        # FIX: LastModified is already a datetime object from boto3; call isoformat() safely
        last_modified = file_info.get("LastModified")
        last_modified_str = last_modified.isoformat() if last_modified else None

        return {
            "success": True,
            "fileId": file_id,
            "size": file_info.get("ContentLength", 0),
            "contentType": file_info.get("ContentType", ""),
            "lastModified": last_modified_str,
            "etag": file_info.get("ETag", "").strip('"'),
            "metadata": metadata,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")