# Registration Form Debugging Steps

## Issue
After filling registration form and clicking submit, it goes to a "new form" instead of the payment page.

## What's Happening
When form validation fails, the system:
1. Redirects to `/?registration_error=1`
2. Opens the registration modal again (this is the "new form" you see)
3. Should display error messages in the modal

## Debugging Steps

### 1. Check Server Logs
When you submit the form, check the terminal/console where Django is running. Look for:

**If validation fails:**
```
❌ Form validation errors: {...}
❌ Form data received: [...]
❌ Files received: [...]
❌ POST data values: {...}
❌ Error message: ...
```

**If registration succeeds:**
```
✅ Registration successful - User: ...
🔄 Redirecting to: /payment/?registration_success=1
✅ Redirect response created: 302
```

### 2. Check Browser Console (F12)
1. Open browser DevTools (F12)
2. Go to Console tab
3. Submit the registration form
4. Look for:
   - `📝 Registration form submitted`
   - `✅ Form submission proceeding - server will handle redirect`
   - `⚠️ Registration error detected in URL - opening modal to show errors`
   - Any JavaScript errors

### 3. Check Network Tab (F12)
1. Open browser DevTools (F12)
2. Go to Network tab
3. Submit the registration form
4. Check the first request (POST to `/`):
   - **Status 302**: Form was valid, redirect is happening
   - **Status 200**: Form validation failed, redirected to homepage
   - **Status 400**: Bad request (CSRF or other issue)

### 4. Check Error Messages in Modal
When the registration modal opens again (the "new form"), check:
- Is there a red error message at the top of the modal?
- What does the error message say?
- Are all required fields filled?

### 5. Common Validation Errors

**Missing Required Fields:**
- First Name
- Last Name
- Father's Name
- Phone Number (must be exactly 10 digits)
- Email (must be valid email format)
- Password (minimum 8 characters)
- Password Confirm (must match password)
- Native Village
- District
- Tehsil
- Current Address
- Profile Picture (image file required)

**Invalid Data:**
- Phone number not exactly 10 digits
- Email not in valid format
- Passwords don't match
- Password less than 8 characters
- Image file too large (>5MB) or invalid format
- Phone number already registered

## What to Do

1. **Fill ALL required fields** in the registration form
2. **Check the error message** when the modal opens again
3. **Fix the errors** shown in the error message
4. **Submit again**

## If Still Not Working

Share with me:
1. What error message appears in the registration modal?
2. What do you see in the server logs?
3. What do you see in the browser console?
4. What do you see in the network tab?

This will help identify the exact issue.

