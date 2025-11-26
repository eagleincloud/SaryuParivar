# OTP Not Working - Troubleshooting Guide

## Common Issues and Solutions

### Issue: Not Receiving SMS Messages

This is usually caused by one of these issues:

## 1. Firebase Billing Not Enabled ⚠️ MOST COMMON

**Error Code**: `auth/billing-not-enabled`

**Solution**:
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: **saryuparivar-acc39**
3. Click **⚙️ Project Settings** → **Usage and billing**
4. Click **Upgrade to Blaze plan** (pay-as-you-go)
5. Add payment method (credit/debit card)
6. Wait 1-2 minutes for activation
7. Then enable Phone Authentication (see step 2)

**Why**: Phone Authentication REQUIRES Blaze plan. Free Spark plan doesn't support SMS.

---

## 2. Phone Authentication Not Enabled

**Error Code**: `auth/configuration-not-found`

**Solution**:
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: **saryuparivar-acc39**
3. Go to **Authentication** → **Sign-in method**
4. Find **Phone** in the list
5. Click **Phone** → Toggle **Enable** to ON
6. Click **Save**

**Note**: Billing must be enabled FIRST before enabling Phone Authentication.

---

## 3. Rate Limiting

**Error Code**: `auth/too-many-requests`

**Solution**:
- Wait 5-10 minutes before trying again
- Firebase limits requests per phone number per hour
- Use different phone number for testing
- Check browser console for retry timer

---

## 4. Invalid Phone Number Format

**Error Code**: `auth/invalid-phone-number`

**Solution**:
- Enter 10-digit phone number (without country code)
- Example: `9898998988` (not `+919898998988`)
- The app automatically adds `+91` country code

---

## 5. reCAPTCHA Issues

**Error Code**: `auth/captcha-check-failed`

**Solution**:
- Refresh the page
- Clear browser cache
- Try in incognito/private mode
- Check browser console for errors

---

## 6. SMS Quota Exceeded

**Error Code**: `auth/quota-exceeded`

**Solution**:
- Check Firebase Console → Usage
- Upgrade plan if needed
- Wait for quota reset (usually daily)
- Contact Firebase support if persistent

---

## Quick Diagnostic Steps

### Step 1: Check Browser Console
1. Open browser Developer Tools (F12)
2. Go to **Console** tab
3. Try sending OTP
4. Look for error messages
5. Common errors:
   - `auth/billing-not-enabled` → Enable billing
   - `auth/configuration-not-found` → Enable Phone Auth
   - `auth/too-many-requests` → Wait and retry
   - `auth/invalid-phone-number` → Check format

### Step 2: Check Firebase Console
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: **saryuparivar-acc39**
3. Check **Authentication** → **Users** tab
4. Check **Authentication** → **Sign-in method** → **Phone**
5. Verify Phone Authentication is enabled

### Step 3: Test with Test Phone Numbers
1. Go to Firebase Console → Authentication → Sign-in method → Phone
2. Scroll to **Phone numbers for testing**
3. Add test number: `+919898998988` with code: `123456`
4. Use this number in app (no SMS sent, uses test code)

---

## Testing Without SMS (Development)

### Use Firebase Test Phone Numbers

1. **Add Test Number in Firebase**:
   - Go to Firebase Console
   - Authentication → Sign-in method → Phone
   - Scroll to "Phone numbers for testing"
   - Add: `+919898998988` with code: `123456`

2. **Use in App**:
   - Enter phone: `9898998988` (10 digits)
   - Click "Request OTP"
   - Enter test code: `123456`
   - No actual SMS sent

---

## Current Configuration

**Firebase Project**: saryuparivar-acc39
**API Key**: AIzaSyBcOdG0hC3BCrhZkxrhxIzWdvc9wdWwHuA
**Auth Domain**: saryuparivar-acc39.firebaseapp.com

---

## Step-by-Step Fix

### If OTP Not Working:

1. **Check Billing** (MOST IMPORTANT):
   ```
   Firebase Console → Project Settings → Usage and billing
   → Upgrade to Blaze plan → Add payment method
   ```

2. **Enable Phone Authentication**:
   ```
   Firebase Console → Authentication → Sign-in method
   → Phone → Enable → Save
   ```

3. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Check Console for errors
   - Look for Firebase error codes

4. **Test with Test Number**:
   - Add test number in Firebase Console
   - Use test code instead of SMS

5. **Verify Phone Format**:
   - Enter 10 digits only
   - App adds +91 automatically

---

## Contact & Support

If issues persist:
1. Check Firebase Console for error logs
2. Review browser console errors
3. Verify billing is enabled
4. Verify Phone Authentication is enabled
5. Try test phone numbers first

---

## Quick Checklist

- [ ] Billing enabled (Blaze plan)
- [ ] Phone Authentication enabled
- [ ] Phone number format correct (10 digits)
- [ ] Not rate limited (wait if needed)
- [ ] Browser console checked for errors
- [ ] Firebase Console checked

---

## Expected Behavior

**When Working Correctly**:
1. Enter phone number (10 digits)
2. Click "Request OTP"
3. Success message: "OTP sent successfully!"
4. OTP input field appears
5. Receive SMS with 6-digit code
6. Enter code and verify
7. Login successful

**If Not Working**:
- Check browser console for error
- Follow troubleshooting steps above
- Most likely: Billing not enabled

