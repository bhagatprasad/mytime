# app/api/middleware.py - CORRECTED
from fastapi import Request
from fastapi.responses import Response
import time
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class AuthHeaderMiddleware:
    """
    Middleware to add authorization headers to responses
    Similar to C# ClarityAuthorize behavior
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:  # ← FIXED: Added self
        # Process request
        start_time = time.time()
        
        # Call the next middleware/endpoint
        response = await call_next(request)
        
        # Add authorization headers if they were set during request processing
        if hasattr(request.state, "auth_headers"):
            for header_name, header_value in request.state.auth_headers.items():
                # Convert header name to proper case
                header_key = header_name
                if header_name.lower() == "authorization":
                    header_key = "Authorization"
                elif header_name.lower() == "authstatus":
                    header_key = "AuthStatus"
                elif header_name.lower() == "storeaccessiblity":
                    header_key = "storeAccessiblity"
                
                response.headers[header_key] = str(header_value)
        
        # Log request (optional)
        process_time = time.time() - start_time
        if process_time > 1:  # Log slow requests
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"Time: {process_time:.3f}s"
            )
        
        return response