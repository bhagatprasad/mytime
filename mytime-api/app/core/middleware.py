# app/api/middleware.py - CORRECTED VERSION
from fastapi import Request
from fastapi.responses import Response
import time
import logging
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)

class AuthHeaderMiddleware:
    """
    Middleware to add authorization headers to responses
    Similar to C# ClarityAuthorize behavior
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        """
        Correct ASGI signature for middleware.
        scope: dict containing request information
        receive: async callable to receive messages
        send: async callable to send messages
        """
        if scope["type"] != "http":
            # If it's not an HTTP request, just pass it through
            await self.app(scope, receive, send)
            return
        
        # Create a Request object from the scope
        request = Request(scope, receive)
        
        # Process the request and get response
        start_time = time.time()
        
        # We need to intercept the response to add headers
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Add authorization headers if they were set during request processing
                if hasattr(request.state, "auth_headers"):
                    headers = dict(message.get("headers", []))
                    
                    for header_name, header_value in request.state.auth_headers.items():
                        # Convert header name to proper case
                        header_key = header_name
                        if header_name.lower() == "authorization":
                            header_key = "Authorization"
                        elif header_name.lower() == "authstatus":
                            header_key = "AuthStatus"
                        elif header_name.lower() == "storeaccessiblity":
                            header_key = "storeAccessiblity"
                        
                        # Convert to bytes for ASGI headers
                        headers[header_key.lower().encode()] = str(header_value).encode()
                    
                    # Update the headers in the message
                    message["headers"] = list(headers.items())
            
            await send(message)
        
        # Call the next middleware/endpoint
        await self.app(scope, receive, send_wrapper)
        
        # Log request (optional)
        process_time = time.time() - start_time
        if process_time > 1:  # Log slow requests
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"Time: {process_time:.3f}s"
            )