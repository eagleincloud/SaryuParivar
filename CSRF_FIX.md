# CSRF Verification Failed - Fix

## Issue
Getting "Forbidden (403) CSRF verification failed. Request aborted." error when submitting registration form.

## Root Cause
The CSRF cookie settings were configured for HTTPS (`CSRF_COOKIE_SECURE = True`), but the site is being accessed via HTTP (localhost:8000). When `CSRF_COOKIE_SECURE = True`, the CSRF cookie can only be sent over HTTPS connections, causing CSRF verification to fail on HTTP.

## Solution

### 1. Updated `pod.env` for Local Development
Changed:
```env
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

This allows CSRF cookies to work over HTTP for local development.

### 2. Fixed Cookie Domain Settings
Updated `settings.py` to properly handle empty cookie domain values:
- Only set `CSRF_COOKIE_DOMAIN` if explicitly provided (not empty string)
- Only set `SESSION_COOKIE_DOMAIN` if explicitly provided (not empty string)

## For Production (EC2)
When deploying to production with HTTPS:
1. Set in `pod.env`:
   ```env
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   CSRF_COOKIE_DOMAIN=saryuparivar.com
   SESSION_COOKIE_DOMAIN=saryuparivar.com
   ```

2. Ensure `CSRF_TRUSTED_ORIGINS` includes your domain:
   ```env
   CSRF_TRUSTED_ORIGINS=http://saryuparivar.com,https://saryuparivar.com,http://www.saryuparivar.com,https://www.saryuparivar.com
   ```

## Testing
1. Restart Django server
2. Clear browser cookies for localhost:8000
3. Try registration form again
4. CSRF error should be resolved

## Status
✅ Fixed CSRF cookie settings for local development
✅ Fixed cookie domain handling
✅ CSRF token should now work properly
