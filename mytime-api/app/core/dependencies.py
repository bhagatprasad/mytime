# app/core/dependencies.py
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from jose import JWTError
import logging
from datetime import datetime
import json
import base64

from app.core.config import settings
from app.core.database import get_db
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)

security = HTTPBearer()

def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current authenticated user - used to protect endpoints
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Please Provide Authorization",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    
    # Enhanced debugging
    logger.info(f"🔐 Authentication attempt")
    logger.info(f"📝 Token preview: {token[:50]}...")
    logger.info(f"🔑 Using SECRET_KEY preview: {settings.SECRET_KEY[:10]}...")
    
    try:
        # Try to manually decode token first to see structure
        try:
            parts = token.split('.')
            if len(parts) == 3:
                # Decode header and payload
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '===').decode('utf-8'))
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '===').decode('utf-8'))
                
                logger.info(f"📋 Token Algorithm: {header.get('alg')}")
                logger.info(f"📋 Token Type: {header.get('typ')}")
                logger.info(f"📋 Payload claims: {list(payload.keys())}")
                
                # Check if token has expired
                if 'exp' in payload:
                    exp_time = datetime.fromtimestamp(payload['exp'])
                    current_time = datetime.utcnow()
                    if exp_time < current_time:
                        logger.warning(f"⏰ Token expired at {exp_time}")
                        raise jwt.ExpiredSignatureError("Token expired")
        except Exception as decode_error:
            logger.warning(f"⚠️ Could not manually decode token: {decode_error}")
        
        # Now verify with JWT library
        logger.info("🔍 Verifying JWT token...")
        
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        logger.info(f"✅ Token verified successfully!")
        
        # Get username from payload (C# uses "name", standard JWT uses "sub")
        username: str = payload.get("name") or payload.get("sub")
        if username is None:
            logger.error("❌ Token missing 'name' or 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no username claim",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        logger.info(f"👤 Username from token: {username}")
        
        # Get user from database via auth service
        # IMPORTANT: Use the same key that AuthService uses
        auth_service = AuthService(settings.SECRET_KEY, db)
        user_info = auth_service.get_user_by_username(username)
        
        if not user_info:
            logger.warning(f"❌ User '{username}' not found in database")
            
            # Debug: List available users
            try:
                from sqlalchemy import text
                query = text("SELECT TOP 5 Email FROM [user]")
                result = db.execute(query)
                users = [row[0] for row in result.fetchall()]
                logger.info(f"👥 Available users in database: {users}")
            except Exception as db_error:
                logger.error(f"❌ Error checking users: {db_error}")
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        logger.info(f"✅ User found: ID={user_info.get('id')}, Active={user_info.get('is_active')}")
        
        # Check if user is active
        if not user_info.get("is_active", True):
            logger.warning(f"⚠️  User '{username}' is not active")
            request.state.auth_headers = {
                "Authorization": token,
                "AuthStatus": "UnAuthorized"
            }
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is not active",
                headers={
                    "Authorization": token,
                    "AuthStatus": "UnAuthorized"
                }
            )
        
        # Success - add authorization headers
        request.state.auth_headers = {
            "Authorization": token,
            "AuthStatus": "Authorized",
            "storeAccessiblity": "Authorized"
        }
        
        logger.info(f"🎉 Authentication successful for {username}")
        
        return {
            "username": username,
            "user_id": user_info.get("id"),
            "email": user_info.get("email"),
            "roles": user_info.get("roles", []),
            "is_active": user_info.get("is_active", True),
            "token": token,
            "department_id": user_info.get("department_id"),
            "role_id": user_info.get("role_id")
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning("⏰ Token expired")
        request.state.auth_headers = {
            "Authorization": token,
            "AuthStatus": "UnAuthorized"
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
            headers={
                "Authorization": token,
                "AuthStatus": "UnAuthorized"
            }
        )
    except jwt.InvalidSignatureError:
        logger.error("❌ Invalid token signature")
        logger.error("💡 Likely cause: SECRET_KEY mismatch between C# and Python")
        request.state.auth_headers = {
            "Authorization": token,
            "AuthStatus": "UnAuthorized"
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token signature",
            headers={
                "Authorization": token,
                "AuthStatus": "UnAuthorized"
            }
        )
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ Invalid token: {str(e)}")
        request.state.auth_headers = {
            "Authorization": token,
            "AuthStatus": "UnAuthorized"
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid token: {str(e)}",
            headers={
                "Authorization": token,
                "AuthStatus": "UnAuthorized"
            }
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"💥 Unexpected authentication error: {str(e)}", exc_info=True)
        request.state.auth_headers = {
            "Authorization": token if 'token' in locals() else "",
            "AuthStatus": "UnAuthorized"
        }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )