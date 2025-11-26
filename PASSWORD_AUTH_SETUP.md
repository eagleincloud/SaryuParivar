# Password-Based Authentication Setup

## Overview

The application now uses **username/password authentication** instead of OTP. Users can:
- Register with email and password
- Login with username/phone number + password
- Reset password via email if forgotten

## Changes Made

### 1. Registration Form
- Added **email** field (required)
- Added **password** field (minimum 8 characters)
- Added **password confirmation** field
- Password is hashed and stored securely

### 2. Login System
- Changed from OTP to **username/phone + password**
- Users can login with either:
  - Username
  - Phone number
- Added "Forgot Password?" link

### 3. Password Reset
- Users can reset password via email
- Enter username/phone number
- Receive password reset link via email
- Set new password

## Configuration

### Email Settings

Add these to your `.env` file (or `pod.env`):

```env
# Email Configuration (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@saryuparivar.com
```

### Gmail Setup (Example)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → 2-Step Verification
   - Click "App passwords"
   - Generate password for "Mail"
   - Use this password in `EMAIL_HOST_PASSWORD`

### Other Email Providers

**For Outlook/Hotmail:**
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**For Yahoo:**
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**For Custom SMTP:**
```env
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
```

## Testing

### Registration
1. Click "Register"
2. Fill in all fields including:
   - Email (required)
   - Password (min 8 characters)
   - Confirm Password
3. Submit form
4. User is auto-logged in and redirected to payment page

### Login
1. Click "Login"
2. Enter username or phone number
3. Enter password
4. Click "Login"
5. Redirected to dashboard

### Password Reset
1. Click "Forgot Password?" on login page
2. Enter username or phone number
3. Check email for reset link
4. Click link in email
5. Set new password
6. Login with new password

## Important Notes

1. **Email is Required**: Users must provide email during registration for password reset to work
2. **Password Security**: Passwords are hashed using Django's default password hashing
3. **OTP Still Available**: OTP login is still available as fallback (Firebase/backend SMS)
4. **Email Must Be Configured**: Password reset won't work without proper email configuration

## Troubleshooting

### Password Reset Email Not Received?
1. Check spam folder
2. Verify email settings in `.env`
3. Check email server logs
4. Ensure user has email in database

### Login Not Working?
1. Verify username/phone number is correct
2. Check password is correct
3. Ensure user account is active
4. Check browser console for errors

### Registration Fails?
1. Ensure all required fields are filled
2. Password must be at least 8 characters
3. Passwords must match
4. Email must be valid format
5. Phone number must be unique

---

**Password-based authentication is now active!** 🔐

