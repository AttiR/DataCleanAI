from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from typing import List
import os

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS", "True").lower() == "true",
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS", "True").lower() == "true"
)

async def send_email_verification(email: str, username: str, verification_url: str):
    """Send email verification email."""
    message = MessageSchema(
        subject="Verify Your Email - AutoDataFix",
        recipients=[email],
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #1976d2, #42a5f5); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">Welcome to AutoDataFix!</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">AI-Powered Data Quality System</p>
            </div>

            <div style="background: white; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {username}!</h2>

                <p style="color: #666; line-height: 1.6; font-size: 16px;">
                    Thank you for signing up for AutoDataFix. To complete your registration and start using our powerful data cleaning and analysis tools, please verify your email address by clicking the button below.
                </p>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}"
                       style="background: #1976d2; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>

                <p style="color: #666; line-height: 1.6; font-size: 14px;">
                    If the button doesn't work, you can copy and paste this link into your browser:
                </p>
                <p style="color: #1976d2; word-break: break-all; font-size: 14px; background: #f5f5f5; padding: 10px; border-radius: 5px;">
                    {verification_url}
                </p>

                <p style="color: #666; line-height: 1.6; font-size: 14px; margin-top: 30px;">
                    This link will expire in 24 hours. If you didn't create an account with AutoDataFix, please ignore this email.
                </p>

                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">

                <p style="color: #999; font-size: 12px; text-align: center; margin: 0;">
                    © 2024 AutoDataFix. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_password_reset(email: str, username: str, reset_url: str):
    """Send password reset email."""
    message = MessageSchema(
        subject="Reset Your Password - AutoDataFix",
        recipients=[email],
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #dc004e, #f48fb1); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">Password Reset Request</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">AutoDataFix Security</p>
            </div>

            <div style="background: white; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {username}!</h2>

                <p style="color: #666; line-height: 1.6; font-size: 16px;">
                    We received a request to reset your password for your AutoDataFix account. If you made this request, click the button below to reset your password.
                </p>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}"
                       style="background: #dc004e; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">
                        Reset Password
                    </a>
                </div>

                <p style="color: #666; line-height: 1.6; font-size: 14px;">
                    If the button doesn't work, you can copy and paste this link into your browser:
                </p>
                <p style="color: #dc004e; word-break: break-all; font-size: 14px; background: #f5f5f5; padding: 10px; border-radius: 5px;">
                    {reset_url}
                </p>

                <p style="color: #666; line-height: 1.6; font-size: 14px; margin-top: 30px;">
                    This link will expire in 1 hour. If you didn't request a password reset, please ignore this email and your password will remain unchanged.
                </p>

                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">

                <p style="color: #999; font-size: 12px; text-align: center; margin: 0;">
                    © 2024 AutoDataFix. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
