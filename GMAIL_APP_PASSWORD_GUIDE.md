# Gmail App Password Setup Guide

## Why App Password?
Gmail requires an App Password when:
- 2-Step Verification is enabled
- Using third-party apps (like Django) to send emails

## Step-by-Step Instructions

### 1. Check if 2-Step Verification is Enabled
- Go to: https://myaccount.google.com/security
- Look for "2-Step Verification" status
- If disabled, enable it first

### 2. Generate App Password
1. Visit: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. You may need to sign in again
3. Under "Select app", choose **Mail**
4. Under "Select device", choose **Other (Custom name)**
5. Type: **Saryu Parivar Website**
6. Click **Generate**
7. You'll see a 16-character password like: `abcd efgh ijkl mnop`
8. **Copy this password** (you can't see it again!)

### 3. Update Configuration
1. Open `pod.env` file
2. Find the line: `EMAIL_HOST_PASSWORD=417BajrangNagar@1`
3. Replace with: `EMAIL_HOST_PASSWORD=abcdefghijklmnop` (remove spaces)
4. Save the file

### 4. Deploy to EC2
```bash
scp -i saryuparivar-key.pem pod.env ec2-user@44.201.152.56:~/Saryu_Pariwar_Web_App/pod.env
```

### 5. Restart Application
```bash
ssh -i saryuparivar-key.pem ec2-user@44.201.152.56
cd ~/Saryu_Pariwar_Web_App
ps aux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -HUP
```

### 6. Test
1. Go to: https://saryuparivar.com/password_reset/
2. Enter your registered email
3. Click "Send Reset Link"
4. Check your email inbox (and spam folder)

## Troubleshooting

### Still not receiving emails?
1. **Check spam folder**
2. **Verify email is registered** in the system
3. **Check server logs** for errors
4. **Test email sending**:
   ```bash
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'Test', 'ouruserverified@gmail.com', ['your-email@example.com'])
   ```

### App Password not working?
1. Make sure you copied the **full 16 characters**
2. **Remove all spaces** from the password
3. Make sure **2-Step Verification is enabled**
4. Try generating a **new App Password**

### Can't access App Passwords page?
- Make sure 2-Step Verification is enabled
- Some Google Workspace accounts may have restrictions
- Contact your Google Workspace admin if needed

## Security Notes
- App Passwords are secure and can be revoked anytime
- Each app should have its own App Password
- Don't share App Passwords
- Revoke old App Passwords if compromised

