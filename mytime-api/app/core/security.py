# app/core/security.py
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jose import JWTError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer()

class ClarityAuthorize:
    """
    FastAPI equivalent of C# ClarityAuthorize attribute
    Can be used as dependency or middleware
    """
    
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error
        self.security = HTTPBearer(auto_error=auto_error)
    
    async def __call__(
        self, 
        request: Request,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Dict[str, Any]:
        """
        Dependency call - validates token and adds headers
        Similar to OnAuthorization in C#
        """
        if not credentials:
            if self.auto_error:
                self._raise_expectation_failed("Please Provide Authorization")
            return None
        
        auth_token = credentials.credentials
        
        if not self._is_valid_token(auth_token):
            if self.auto_error:
                # Add headers similar to C#
                self._add_response_headers(request, auth_token, "UnAuthorized")
                self._raise_forbidden("Invalid Token")
            return None
        
        # Valid token
        self._add_response_headers(request, auth_token, "Authorized")
        
        # Return user info from token
        user_info = self._get_user_info_from_token(auth_token)
        return {
            "token": auth_token,
            "user_info": user_info,
            "is_authenticated": True
        }
    
    def _is_valid_token(self, auth_token: str) -> bool:
        """Check if token is valid"""
        return self._check_token_is_valid(auth_token)
    
    def _check_token_is_valid(self, token: str) -> bool:
        """Check token expiration"""
        try:
            token_ticks = self._get_token_expiration_time(token)
            token_date = datetime.fromtimestamp(token_ticks)
            now = datetime.utcnow()
            is_valid = token_date >= now
            
            if not is_valid:
                logger.warning(f"Token expired. Token date: {token_date}, Now: {now}")
            
            return is_valid
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False
    
    def _get_token_expiration_time(self, token: str) -> int:
        """Get token expiration time from JWT"""
        try:
            # Decode without verification to get payload
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM],
                options={"verify_signature": False}
            )
            token_exp = payload.get("exp")
            if not token_exp:
                logger.error("No expiration time in token")
                raise ValueError("No expiration time in token")
            return int(token_exp)
        except Exception as e:
            logger.error(f"Error getting token expiration: {e}")
            raise
    
    def _get_user_info_from_token(self, token: str) -> Dict[str, Any]:
        """Extract user information from token"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM],
                options={"verify_signature": False}
            )
            return {
                "username": payload.get("sub") or payload.get("name"),
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "roles": payload.get("roles", []),
                "exp": payload.get("exp"),
                "iat": payload.get("iat")
            }
        except Exception as e:
            logger.error(f"Error extracting user info from token: {e}")
            return {}
    
    def _add_response_headers(self, request: Request, auth_token: str, auth_status: str):
        """Add authorization headers to response"""
        # Store headers to be added in middleware or response
        request.state.auth_headers = {
            "Authorization": auth_token,
            "AuthStatus": auth_status,
            "storeAccessiblity": auth_status
        }
    
    def _raise_expectation_failed(self, message: str):
        """Raise 417 Expectation Failed error"""
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    def _raise_forbidden(self, message: str):
        """Raise 403 Forbidden error"""
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"}
        )

# Create instance for easy import
clarity_authorize = ClarityAuthorize()