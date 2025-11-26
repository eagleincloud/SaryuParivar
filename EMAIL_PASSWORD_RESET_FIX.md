# Email Password Reset Fix

## Issue
Not receiving emails when clicking "Forgot Password"

## Root Cause
Gmail requires an **App Password** when 2-Step Verification is enabled. The current password in `pod.env` is not an App Password.

## Error Message
```
SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required')
```

## Solution: Generate Gmail App Password

### Step 1: Enable 2-Step Verification (if not already enabled)
1. Go to: https://myaccount.google.com/security
2. Under "Signing in to Google", click **2-Step Verification**
3. Follow the steps to enable it

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Or: Google Account → Security → 2-Step Verification → App passwords
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Enter name: **Saryu Parivar Website**
6. Click **Generate**
7. **Copy the 16-character password** (no spaces)

### Step 3: Update pod.env
Replace the current password with the App Password:

```env
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

**Important**: Remove spaces from the App Password when adding to pod.env

### Step 4: Restart Application
```bash
# On EC2
sudo systemctl restart gunicorn
# or
ps aux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -HUP
```

## Alternative: Use Console Backend (for testing only)

If you want to test without setting up App Password, you can temporarily use console backend:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This will print emails to the console instead of sending them.

## Testing Email Configuration

### Test on Local:
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'ouruserverified@gmail.com', ['test@example.com'], fail_silently=False)
```

### Test on EC2:
```bash
cd ~/Saryu_Pariwar_Web_App
source venv/bin/activate
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'ouruserverified@gmail.com', ['test@example.com'], fail_silently=False)
```

## Current Email Configuration

- **EMAIL_BACKEND**: `django.core.mail.backends.smtp.EmailBackend`
- **EMAIL_HOST**: `smtp.gmail.com`
- **EMAIL_PORT**: `587`
- **EMAIL_USE_TLS**: `True`
- **EMAIL_HOST_USER**: `ouruserverified@gmail.com`
- **EMAIL_HOST_PASSWORD**: `417BajrangNagar@1` (needs to be App Password)
- **DEFAULT_FROM_EMAIL**: `ouruserverified@gmail.com`

## Quick Fix Steps

1. **Generate Gmail App Password** (see steps above)
2. **Update pod.env** with new App Password
3. **Sync to EC2**:
   ```bash
   scp -i saryuparivar-key.pem pod.env ec2-user@44.201.152.56:~/Saryu_Pariwar_Web_App/pod.env
   ```
4. **Restart Gunicorn** on EC2
5. **Test password reset** again

## Notes

- App Passwords are 16 characters (may be shown with spaces, remove them)
- App Passwords are different from your regular Gmail password
- You can have multiple App Passwords for different applications
- If you change your Gmail password, App Passwords still work
- App Passwords can be revoked if needed

## Status
⚠️ **Action Required**: Generate Gmail App Password and update `pod.env`

