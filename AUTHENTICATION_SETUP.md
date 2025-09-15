# Authentication Setup Guide

This guide will help you set up the authentication system for AutoDataFix.

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database
DATABASE_URL=sqlite:///./database/autodatafix.db

# Security
SECRET_KEY=your-secret-key-here-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Email Settings (for Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True

# Debug
DEBUG=True
```

### 3. Email Configuration

To enable email verification and password reset:

1. **Gmail Setup:**
   - Enable 2-factor authentication on your Gmail account
   - Generate an App Password: Google Account → Security → 2-Step Verification → App passwords
   - Use the App Password as `MAIL_PASSWORD` in your `.env` file

2. **Other Email Providers:**
   - Update the `MAIL_SERVER`, `MAIL_PORT`, `MAIL_STARTTLS`, and `MAIL_SSL_TLS` settings accordingly

### 4. Database Migration

The User model has been updated with new fields. You may need to recreate the database:

```bash
# Remove existing database
rm database/autodatafix.db

# Start the backend (this will create new tables)
python -m uvicorn app.main:app --reload
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Frontend

```bash
npm start
```

## Features Implemented

### Backend Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ Email verification system
- ✅ Password reset functionality
- ✅ User registration and login
- ✅ Protected API endpoints
- ✅ User-specific data isolation
- ✅ Account lockout after failed attempts
- ✅ Email templates for verification and password reset

### Frontend Features

- ✅ Beautiful, responsive login/register pages
- ✅ Email verification page
- ✅ Protected routes
- ✅ User profile menu in navigation
- ✅ Authentication context and state management
- ✅ Automatic token refresh
- ✅ Email verification status indicators
- ✅ Password strength validation
- ✅ Error handling and user feedback

### Security Features

- ✅ Password complexity requirements
- ✅ JWT token expiration
- ✅ Account lockout mechanism
- ✅ Email verification requirement
- ✅ Secure password reset tokens
- ✅ User data isolation
- ✅ CORS protection

## Usage

### 1. User Registration

1. Navigate to `/register`
2. Fill in the registration form
3. Check your email for verification link
4. Click the verification link to activate your account

### 2. User Login

1. Navigate to `/login`
2. Enter your email and password
3. You'll be redirected to the dashboard

### 3. Password Reset

1. Click "Forgot your password?" on the login page
2. Enter your email address
3. Check your email for reset instructions

### 4. Data Access

- Only authenticated users can access the application
- Users can only see and manage their own datasets
- Email verification is required for full access

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/verify-email` - Email verification
- `POST /api/v1/auth/resend-verification` - Resend verification email
- `POST /api/v1/auth/request-password-reset` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password
- `POST /api/v1/auth/change-password` - Change password
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

### Protected Endpoints

All dataset, analysis, and cleaning endpoints now require authentication:
- `GET /api/v1/datasets` - List user's datasets
- `POST /api/v1/datasets/upload` - Upload dataset
- `GET /api/v1/datasets/{id}` - Get dataset details
- `DELETE /api/v1/datasets/{id}` - Delete dataset
- And all other existing endpoints...

## Troubleshooting

### Common Issues

1. **Email not sending:**
   - Check your email credentials in `.env`
   - Ensure 2FA is enabled and App Password is used
   - Check firewall/antivirus blocking SMTP

2. **Database errors:**
   - Delete `database/autodatafix.db` and restart backend
   - Check database permissions

3. **Frontend not connecting:**
   - Ensure backend is running on port 8000
   - Check CORS settings in backend

4. **Token errors:**
   - Clear browser localStorage
   - Check SECRET_KEY is set in backend

### Support

If you encounter any issues, check the console logs for both frontend and backend, and ensure all environment variables are properly set.
