# auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application_user import ApplicationUser
from app.models.auth_response import AuthResponse
from app.models.change_password import ChangePassword
from app.models.reset_password import ResetPassword
from app.models.user_authentication import UserAuthentication
from app.services.auth_service import AuthService


logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal Server Error"}
    }
)

# Configuration
USED_GENERATES_TOKEN_KEY = "your-secret-key-change-in-production"

# Dependency for AuthService
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(USED_GENERATES_TOKEN_KEY, db)

@router.post(
    "/AuthenticateUser",
    response_model=AuthResponse,
    summary="Authenticate User",
    description="Authenticate user with username and password"
)
def authenticate_user(
    user_auth: UserAuthentication,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user with username and password.
    Returns JWT token if authentication is successful.
    """
    try:
        response = auth_service.authenticate_user(
            user_auth.username, 
            user_auth.password
        )
        
        # Check authentication result
        if not response.valid_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not response.valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        if not response.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is not active"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Authentication error: {str(ex)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(ex)}"
        )

@router.post(
    "/GenarateUserClaims",
    response_model=ApplicationUser,
    summary="Generate User Claims",
    description="Generate user claims from JWT token"
)
def generate_user_claims(
    auth_response: AuthResponse,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Generate user claims from JWT token.
    Validates the token and returns user information.
    """
    try:
        response = auth_service.generate_user_claims(auth_response)
        
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or token is invalid"
            )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as ex:
        logger.error(f"Generate claims error: {str(ex)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate user claims: {str(ex)}"
        )

@router.get(
    "/ForgotPasswordAsync/{user_name}",
    response_model=ApplicationUser,
    summary="Forgot Password",
    description="Initiate password reset process"
)
def forgot_password_async(
    user_name: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Forgot password endpoint.
    Returns user information if user exists and is active.
    """
    try:
        response = auth_service.forgot_password(user_name)
        
        if not response:
            # Return empty response instead of 404 for security
            return ApplicationUser(id=0)
        
        return response
        
    except Exception as ex:
        logger.error(f"Forgot password error: {str(ex)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process forgot password: {str(ex)}"
        )

@router.post(
    "/ResetPasswordAsync",
    response_model=Dict[str, Any],
    summary="Reset Password",
    description="Reset user password"
)
def reset_password_async(
    reset_password: ResetPassword,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Reset user password.
    Requires user ID and new password.
    """
    try:
        success = auth_service.reset_password_async(reset_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reset password. User may not exist."
            )
        
        return {"success": True, "message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Reset password error: {str(ex)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(ex)}"
        )

@router.post(
    "/ChangePasswordAsync",
    response_model=Dict[str, Any],
    summary="Change Password",
    description="Change user password with old password verification"
)
def change_password_async(
    change_password: ChangePassword,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Change user password.
    Requires username, old password, and new password.
    """
    try:
        success = auth_service.change_password_async(change_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password. Invalid old password or user not found."
            )
        
        return {"success": True, "message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Change password error: {str(ex)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(ex)}"
        )