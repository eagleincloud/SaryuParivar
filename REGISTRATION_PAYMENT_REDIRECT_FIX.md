# Registration Payment Redirect Fix

## Issue
After successful registration, user is not being redirected to the payment page - stays on home/root page.

## Root Cause
The `registration_page` view was checking if user is authenticated at the start and redirecting authenticated users to dashboard, which could interfere with the registration flow.

## Solution

### 1. Fixed Authentication Check in `registration_page`
- Only redirect authenticated users on **GET** requests
- Allow POST requests to proceed even if user becomes authenticated during registration
- This ensures the redirect to payment page works correctly

### 2. Enhanced Redirect
- Using `HttpResponseRedirect` for explicit redirect
- Redirect URL: `/payment/?registration_success=1`
- Added debug logging to track redirect

## Code Changes

### `administration/views.py` - `registration_page` function:

```python
def registration_page(request):
    # Don't redirect authenticated users if this is a POST (they might be registering)
    # Only redirect if it's a GET request from an authenticated user
    if request.method == 'GET' and request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    
    if request.method == 'POST':
        # ... registration logic ...
        # After successful registration:
        login(request, user)
        # ... create payment transaction ...
        return HttpResponseRedirect('/payment/?registration_success=1')
```

## Registration Flow

1. **User submits registration form** → POST to `/`
2. **`homepage` view** → Calls `registration_page(request)`
3. **`registration_page` view**:
   - Validates form
   - Creates user
   - Creates payment transaction
   - Auto-logs in user
   - **Redirects to `/payment/?registration_success=1`**
4. **Payment page** → Shows payment form and QR code

## Testing

1. Go to homepage
2. Click "Register"
3. Fill registration form
4. Submit form
5. **Expected**: Should redirect to `/payment/` page
6. **Payment page should show**:
   - Success message
   - Payment banner (if pending)
   - QR code
   - Payment amount
   - Transaction ID

## Status
✅ Fixed authentication check to allow POST requests
✅ Using `HttpResponseRedirect` for explicit redirect
✅ Redirect URL includes `registration_success=1` parameter
✅ Debug logging added

