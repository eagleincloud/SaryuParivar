# OTP Login Fix

## Issues Fixed

### 1. JavaScript Scope Issues
- **Problem**: Firebase variables (`auth`, `recaptchaVerifier`, `confirmationResult`) were in module scope but functions needed global access
- **Fix**: Added global accessor functions to expose module variables:
  - `window.firebaseAuth` - Firebase auth instance
  - `window.firebaseRecaptchaVerifier()` - Get reCAPTCHA verifier
  - `window.firebaseSetRecaptchaVerifier()` - Set reCAPTCHA verifier
  - `window.firebaseConfirmationResult()` - Get confirmation result
  - `window.firebaseSetConfirmationResult()` - Set confirmation result

### 2. Error Handling Improvements
- Added better error messages for specific Firebase errors:
  - `auth/invalid-verification-code` - Invalid OTP
  - `auth/code-expired` - OTP expired
  - `auth/session-expired` - Session expired
- Added CSRF token validation
- Added confirmation result validation before verification

### 3. reCAPTCHA Initialization
- Fixed reCAPTCHA initialization to use global auth instance
- Added proper cleanup on errors
- Fixed modal event listener

## Testing OTP Login

### Steps:
1. **Open Login Modal**: Click "Login" button on homepage
2. **Enter Phone Number**: Enter 10-digit phone number (e.g., 9876543210)
3. **Click "Send OTP"**: 
   - Should check if user exists
   - Should initialize reCAPTCHA
   - Should send OTP via Firebase
   - Should show OTP input field
4. **Enter OTP**: Enter 6-digit OTP received on phone
5. **Click "Verify OTP"**:
   - Should verify with Firebase
   - Should send token to backend
   - Should login user
   - Should redirect to dashboard

### Common Issues & Solutions

#### Issue: "Firebase Authentication not initialized"
- **Solution**: Refresh the page and try again
- **Check**: Browser console for Firebase initialization errors

#### Issue: "reCAPTCHA verification failed"
- **Solution**: Refresh the page and try again
- **Check**: Ensure reCAPTCHA container is visible (even if invisible)

#### Issue: "User not found"
- **Solution**: User must be registered first
- **Check**: Phone number matches registered number

#### Issue: "Too many requests"
- **Solution**: Wait 60 seconds before trying again
- **Check**: Rate limiting is working (max 5 requests per hour)

#### Issue: "Billing not enabled" or "Configuration not found"
- **Solution**: Enable billing and Phone Authentication in Firebase Console
- **See**: `FIREBASE_SETUP_INSTRUCTIONS.md` for detailed steps

## Debugging

### Check Browser Console (F12):
1. Look for Firebase initialization message: "Firebase initialized successfully"
2. Check for any error messages when clicking "Send OTP"
3. Check for any error messages when verifying OTP
4. Look for network errors in Network tab

### Common Console Messages:
- ✅ `Firebase initialized successfully` - Good
- ✅ `reCAPTCHA verified` - Good
- ❌ `Error initializing Firebase` - Check Firebase config
- ❌ `Error initializing reCAPTCHA` - Check reCAPTCHA container
- ❌ `Firebase error: auth/billing-not-enabled` - Enable billing
- ❌ `Firebase error: auth/configuration-not-found` - Enable Phone Auth

## Firebase Setup Requirements

1. **Billing Enabled**: Blaze (pay-as-you-go) plan required
2. **Phone Authentication Enabled**: In Firebase Console
3. **reCAPTCHA Configured**: For web apps
4. **Valid API Key**: In firebase_config.py

## Status

✅ **Fixed**: JavaScript scope issues
✅ **Fixed**: Error handling
✅ **Fixed**: reCAPTCHA initialization
✅ **Fixed**: CSRF token validation

---

**OTP login should now work correctly!** 🎉

If you still encounter issues, check the browser console (F12) for detailed error messages.

