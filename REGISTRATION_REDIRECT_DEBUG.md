# Registration Redirect Debug Guide

## Issue
After filling registration form and clicking submit, it redirects back to registration form instead of payment page.

## Possible Causes

### 1. Form Validation Errors
If the form has validation errors, it redirects to `/?registration_error=1` which re-opens the registration modal.

**Check:**
- Look at server logs for "❌ Form validation errors"
- Check browser console for any JavaScript errors
- Verify all required fields are filled correctly

### 2. Payment Page Access Issue
If the payment page returns an error (400), the redirect might fail.

**Check:**
- Server logs for payment page errors
- Verify user is authenticated after registration
- Check if payment transaction is created

### 3. Redirect Chain Issue
The redirect might be happening but then something redirects back.

**Check:**
- Server logs for redirect messages
- Browser network tab to see redirect chain
- Check if homepage is redirecting authenticated users

## Debug Steps

### 1. Check Server Logs
Look for these messages in server logs:
```
✅ User auto-logged in: [username]
✅ Registration successful - User: [username], Transaction: TXN[number]
✅ Redirecting to payment page: /payment/
🔄 Redirecting to: /payment/?registration_success=1
✅ Redirect response created: 302
```

If you see "❌ Form validation errors", check what fields are failing.

### 2. Check Browser Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Submit registration form
4. Check the request/response:
   - First request should be POST to `/`
   - Response should be 302 redirect to `/payment/`
   - Second request should be GET to `/payment/`
   - Response should be 200 with payment page HTML

### 3. Check Form Validation
If form validation is failing, you'll see:
- Error messages in the registration modal
- Server logs showing validation errors
- Redirect to `/?registration_error=1`

**Common validation errors:**
- Missing required fields
- Invalid phone number format
- Password mismatch
- Invalid email format
- Image upload issues

### 4. Test Payment Page Directly
After registration, try accessing `/payment/` directly:
- If you see payment page → Redirect is working
- If you see error → Payment page has an issue

## Fixes Applied

1. **Enhanced Logging**: Added detailed logging for form validation and redirect
2. **Better Error Messages**: More specific error messages for validation failures
3. **Redirect Debug**: Added logging for redirect response

## Next Steps

1. Check server logs when submitting registration form
2. Look for "❌ Form validation errors" or "✅ Registration successful"
3. If validation errors, fix the form fields
4. If successful, check if redirect is happening
5. Verify payment page is accessible

