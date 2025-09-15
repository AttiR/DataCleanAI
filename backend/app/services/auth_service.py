from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
    verify_email_token,
    verify_password_reset_token
)
from app.core.email import send_email_verification, send_password_reset
from app.core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()

        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        verification_token = create_email_verification_token(user_data.email)

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            email_verification_token=verification_token,
            email_verification_expires=datetime.utcnow() + timedelta(hours=24)
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    async def send_verification_email(self, user: User):
        """Send email verification to user."""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}"
        await send_email_verification(user.email, user.username, verification_url)

    def verify_email(self, token: str) -> User:
        """Verify user email with token."""
        try:
            email = verify_email_token(token)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )

        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )

        # Check if token is still valid
        if user.email_verification_expires and user.email_verification_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token has expired"
            )

        user.is_email_verified = True
        user.email_verification_token = None
        user.email_verification_expires = None
        self.db.commit()

        return user

    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password."""
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to too many failed login attempts"
            )

        if not verify_password(password, user.hashed_password):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            self.db.commit()

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check if email is verified (unless in development mode with auto-verification)
        from app.core.config import settings
        enable_email_in_dev = getattr(settings, 'ENABLE_EMAIL_IN_DEV', False)

        if not user.is_email_verified and not (settings.DEBUG and not enable_email_in_dev):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please verify your email address before logging in. Check your inbox for a verification link."
            )

        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        self.db.commit()

        return user

    def create_access_token_for_user(self, user: User) -> str:
        """Create access token for authenticated user."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username
        }
        return create_access_token(token_data)

    async def request_password_reset(self, email: str):
        """Request password reset for user."""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            # Don't reveal if email exists or not for security
            return

        reset_token = create_password_reset_token(email)
        user.password_reset_token = reset_token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        self.db.commit()

        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        await send_password_reset(user.email, user.username, reset_url)

    def reset_password(self, token: str, new_password: str) -> User:
        """Reset user password with token."""
        try:
            email = verify_password_reset_token(token)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if token is still valid
        if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )

        # Update password
        user.hashed_password = get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.last_password_change = datetime.utcnow()
        self.db.commit()

        return user

    def change_password(self, user: User, current_password: str, new_password: str) -> User:
        """Change user password."""
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        user.hashed_password = get_password_hash(new_password)
        user.last_password_change = datetime.utcnow()
        self.db.commit()

        return user

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_user_by_email(self, email: str) -> User:
        """Get user by email."""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
