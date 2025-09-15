from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.rate_limiting import (
    check_rate_limit,
    login_rate_limiter,
    register_rate_limiter,
    password_reset_rate_limiter,
    get_client_ip
)
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    EmailVerificationRequest,
    EmailVerification,
    PasswordResetRequest,
    PasswordReset,
    PasswordChange
)
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    print(f"Registration request received: {user_data}")

    # Check rate limit (disabled in development)
    if not settings.DEBUG:
        check_rate_limit(request, register_rate_limiter)

    auth_service = AuthService(db)

    # Create user
    user = auth_service.register_user(user_data)

    # Check if email should be sent in development mode
    enable_email_in_dev = getattr(settings, 'ENABLE_EMAIL_IN_DEV', False)

    if settings.DEBUG and not enable_email_in_dev:
        # Auto-verify in development mode when email is disabled
        user.is_email_verified = True
        db.commit()
        print(f"User {user.username} auto-verified in development mode (email disabled)")
    else:
        # Send verification email (in production or when email is enabled in dev)
        try:
            background_tasks.add_task(auth_service.send_verification_email, user)
            print(f"Verification email queued for {user.username}")
        except Exception as e:
            print(f"Error queuing verification email: {e}")
            # In case of email error, still mark as verified in development
            if settings.DEBUG:
                user.is_email_verified = True
                db.commit()
                print(f"User {user.username} auto-verified due to email error")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_email_verified=user.is_email_verified,
        created_at=user.created_at,
        last_login=user.last_login
    )

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    # Check rate limit
    check_rate_limit(request, login_rate_limiter)

    auth_service = AuthService(db)

    # Authenticate user
    user = auth_service.authenticate_user(user_credentials.email, user_credentials.password)

    # Create access token
    access_token = auth_service.create_access_token_for_user(user)

    return Token(access_token=access_token, token_type="bearer")

@router.post("/verify-email", response_model=dict)
async def verify_email(
    verification_data: EmailVerification,
    db: Session = Depends(get_db)
):
    """Verify user email with token."""
    auth_service = AuthService(db)

    user = auth_service.verify_email(verification_data.token)

    return {
        "message": "Email verified successfully",
        "user": UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_email_verified=user.is_email_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
    }

@router.post("/resend-verification", response_model=dict)
async def resend_verification_email(
    email_data: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resend email verification."""
    auth_service = AuthService(db)

    try:
        user = auth_service.get_user_by_email(email_data.email)
        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )

        # Generate new verification token
        from app.core.security import create_email_verification_token
        from datetime import datetime, timedelta

        user.email_verification_token = create_email_verification_token(user.email)
        user.email_verification_expires = datetime.utcnow() + timedelta(hours=24)
        db.commit()

        # Send verification email in background
        background_tasks.add_task(auth_service.send_verification_email, user)

        return {"message": "Verification email sent successfully"}

    except HTTPException:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists and is not verified, a verification email has been sent"}

@router.post("/request-password-reset", response_model=dict)
async def request_password_reset(
    email_data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """Request password reset."""
    # Check rate limit
    check_rate_limit(request, password_reset_rate_limiter)

    auth_service = AuthService(db)

    # Send password reset email in background (always return success for security)
    background_tasks.add_task(auth_service.request_password_reset, email_data.email)

    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password", response_model=dict)
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password with token."""
    auth_service = AuthService(db)

    user = auth_service.reset_password(reset_data.token, reset_data.new_password)

    return {"message": "Password reset successfully"}

@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    auth_service = AuthService(db)

    auth_service.change_password(
        current_user,
        password_data.current_password,
        password_data.new_password
    )

    return {"message": "Password changed successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_email_verified=current_user.is_email_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )

@router.post("/logout", response_model=dict)
async def logout():
    """Logout user (client should discard token)."""
    return {"message": "Logged out successfully"}
