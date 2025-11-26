# Login Error Debugging Guide

## Common Login Errors and Solutions

### 1. "User not found" Error
**Cause**: Username/phone/email doesn't exist in database
**Solution**:
- Check if user is registered
- Try using username (auto-generated: `firstname_phonenumber`)
- Try using phone number (10 digits)
- Try using email (if provided during registration)

### 2. "Invalid password" Error
**Cause**: Password doesn't match
**Solution**:
- Check if password is correct
- Ensure no extra spaces
- Try resetting password via "Forgot Password" link

### 3. CSRF Error (403 Forbidden)
**Cause**: CSRF token missing or invalid
**Solution**:
- Clear browser cookies
- Refresh the page
- Try incognito/private window
- Ensure accessing via HTTPS

### 4. "An error occurred during login" Error
**Cause**: Server-side error
**Solution**:
- Check server logs
- Try again after a few seconds
- Contact support if persists

## Improved Error Handling

The login view now includes:
- ✅ Better error messages
- ✅ Exception handling with traceback
- ✅ Improved email lookup (checks if email contains '@')
- ✅ More detailed error responses

## Testing Login

### Test with Username:
1. Use auto-generated username (e.g., `firstname_phonenumber`)
2. Enter password
3. Click Login

### Test with Phone Number:
1. Enter 10-digit phone number
2. Enter password
3. Click Login

### Test with Email:
1. Enter email address (must contain '@')
2. Enter password
3. Click Login

## Debugging Steps

1. **Check Browser Console** (F12 → Console):
   - Look for JavaScript errors
   - Check network requests
   - Verify CSRF token is present

2. **Check Network Tab** (F12 → Network):
   - Find the `/login/` request
   - Check request payload
   - Check response status and message

3. **Check Server Logs**:
   ```bash
   tail -f /tmp/gunicorn_error.log
   ```

4. **Test User Exists**:
   ```python
   from administration.models import CustomUser
   user = CustomUser.objects.filter(username='test').first()
   # or
   user = CustomUser.objects.filter(phone_number='1234567890').first()
   # or
   user = CustomUser.objects.filter(email='test@example.com').first()
   ```

## Common Issues

### Issue: Email lookup fails
- **Fix**: Email lookup now checks if input contains '@' before attempting lookup
- **Note**: Empty emails won't cause errors

### Issue: Multiple users with same email
- **Fix**: Uses `.first()` to get first matching user
- **Note**: Should ensure email uniqueness in future

### Issue: Case sensitivity
- **Fix**: Email lookup is case-insensitive
- **Note**: Username and phone are case-sensitive

## Next Steps

If you're still getting errors:
1. Share the exact error message
2. Check browser console for errors
3. Check network tab for request/response details
4. Try different login methods (username/phone/email)

