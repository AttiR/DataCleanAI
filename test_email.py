#!/usr/bin/env python3
"""
Email Testing Script for AutoDataFix
This script helps you test email functionality before configuring real SMTP settings.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
project_root = Path(__file__).parent
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

async def test_email_configuration():
    """Test email configuration and sending."""
    from app.core.email import send_email_verification
    from app.core.config import settings

    print("🔧 Testing Email Configuration...")
    print(f"📧 Mail Server: {settings.MAIL_SERVER}")
    print(f"📧 Mail Port: {settings.MAIL_PORT}")
    print(f"📧 Mail Username: {settings.MAIL_USERNAME}")
    print(f"📧 Mail From: {settings.MAIL_FROM}")
    print(f"🔒 Use Credentials: {settings.USE_CREDENTIALS}")
    print()

    # Test email sending
    test_email = "test@example.com"
    test_username = "TestUser"
    test_verification_url = "http://localhost:3000/verify-email?token=test-token-123"

    try:
        print("📤 Attempting to send test email...")
        await send_email_verification(test_email, test_username, test_verification_url)
        print("✅ Email sent successfully!")
        print(f"📧 Check {test_email} for the verification email")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print()
        print("🔧 Common issues and solutions:")
        print("1. Gmail App Password: Make sure you're using an App Password, not your regular password")
        print("2. 2FA Required: Enable 2-Factor Authentication on your Gmail account")
        print("3. Less Secure Apps: Enable 'Less secure app access' (not recommended)")
        print("4. SMTP Settings: Verify the SMTP server and port settings")
        print()
        print("📝 To get Gmail App Password:")
        print("1. Go to Google Account settings")
        print("2. Security → 2-Step Verification")
        print("3. App passwords → Generate app password")
        print("4. Use the generated password in MAIL_PASSWORD")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_email_configuration())
