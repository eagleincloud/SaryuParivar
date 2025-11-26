# Manual Testing Guide

## Server Status
✅ Server running at: http://127.0.0.1:8000/

## Test 1: Registration and Payment Upload

### Steps:
1. **Open Browser**: Go to http://127.0.0.1:8000/
2. **Click Register**: Click the "Register" button
3. **Fill Form**:
   - Enter name, surname, father's name
   - Enter phone number (10 digits)
   - Enter address details
   - Upload profile picture (optional)
   - Submit form
4. **Payment Modal**: After registration, payment modal should appear automatically
5. **Upload Payment Proof**:
   - View QR code and UPI ID
   - Upload payment proof (screenshot/photo)
   - Click "Submit Payment Proof"
6. **Verify**:
   - ✅ Payment transaction created in database
   - ✅ Admin notified (check admin panel)
   - ✅ Success message displayed

### Expected Results:
- ✅ User created with `payment_done = False`
- ✅ PaymentTransaction created with `status = 'pending'`
- ✅ Payment modal appears after registration
- ✅ Payment proof uploads successfully
- ✅ Admin notification triggered

---

## Test 2: OTP Login

### Steps:
1. **Open Browser**: Go to http://127.0.0.1:8000/
2. **Click Login**: Click the "Login" button
3. **Enter Phone**: Enter registered phone number (10 digits)
4. **Request OTP**: Click "Request OTP"
5. **Verify OTP Sent**:
   - Check for success message
   - OTP input field should appear
   - Check OTP request counter (should show X/5)
6. **Enter OTP**: Enter 6-digit OTP received via SMS
7. **Verify OTP**: Click "Verify OTP"
8. **Check Login**:
   - Should redirect to /dashboard/
   - Payment banner should appear if payment pending

### Expected Results:
- ✅ OTP sent successfully via Firebase
- ✅ Rate limiting works (5 requests/hour)
- ✅ OTP verification successful
- ✅ User logged in
- ✅ Redirected to dashboard
- ✅ Payment banner shows if payment pending

### OTP Rate Limiting:
- First 5 requests: ✅ Allowed
- 6th request: ⚠️ Blocked (shows retry timer)
- Counter resets after 60 minutes

---

## Test 3: Admin Verification

### Steps:
1. **Login as Admin**: Go to http://127.0.0.1:8000/admin/
2. **Navigate**: Go to "Administration" → "Payment Transactions"
3. **Find Pending Payment**:
   - Look for payments with status "Pending Verification"
   - Check "Notification Status" column
   - "⚠️ NEW - Needs Review" = New payment with proof
4. **View Payment**:
   - Click on payment to view details
   - Check payment proof image (if uploaded)
   - View transaction details
5. **Verify Payment**:
   - Change "Payment status" to "Completed"
   - Optionally add remarks
   - Click "Save"
6. **Verify Result**:
   - Check success message
   - Verify `user.payment_done = True`
   - Verify `payment.verified_by` and `verified_at` set

### Expected Results:
- ✅ Pending payments visible in admin panel
- ✅ Payment proof visible (if uploaded)
- ✅ Admin can verify payment
- ✅ User access automatically updated
- ✅ Verification details recorded

### Alternative: Bulk Action
- Select multiple payments
- Choose "Verify selected payments" from actions dropdown
- Click "Go"
- All selected payments verified at once

---

## Test 4: Payment Banner Display

### Test Banner Appearance (Payment Pending):

1. **Login as User with Pending Payment**:
   - Use a user account with `payment_done = False`
   - Login via OTP
2. **Check Dashboard**:
   - Banner should appear at top of page
   - Banner text: "Payment Verification Pending"
   - Shows transaction ID
   - Has "View Payment Status" button
3. **Check All Pages**:
   - Dashboard home: ✅ Banner shows
   - All Profiles page: ✅ Banner shows
   - My Profile page: ✅ Banner shows
   - Payment page: ✅ Banner shows

### Test Banner Removal (Payment Verified):

1. **Admin Verifies Payment** (as in Test 3)
2. **User Logs Out**: Click logout
3. **User Logs In Again**: Login via OTP
4. **Check Dashboard**:
   - Banner should NOT appear
   - No payment warning messages
   - Full access to all features

### Expected Results:
- ✅ Banner shows when `payment_done = False`
- ✅ Banner shows when payment status is 'pending'
- ✅ Banner appears on ALL dashboard pages
- ✅ Banner disappears after admin verification
- ✅ Banner does not show when `payment_done = True`

---

## Complete End-to-End Test

### Full Workflow:

1. **Registration**:
   ```
   User registers → Payment transaction created → Payment modal appears
   ```

2. **Payment Upload**:
   ```
   User uploads proof → Admin notified → Status: 'pending'
   ```

3. **Login**:
   ```
   User logs in via OTP → Sees payment banner → Has limited access
   ```

4. **Admin Review**:
   ```
   Admin sees notification → Reviews payment → Verifies payment
   ```

5. **Access Update**:
   ```
   User.payment_done = True → Banner removed → Full access granted
   ```

---

## Verification Checklist

### Registration ✅
- [ ] User can register successfully
- [ ] Payment transaction created automatically
- [ ] Payment modal appears after registration
- [ ] User can upload payment proof

### OTP Login ✅
- [ ] OTP sent successfully
- [ ] Rate limiting works (5 requests/hour)
- [ ] OTP verification works
- [ ] User logged in successfully
- [ ] Redirected to dashboard

### Payment Banner ✅
- [ ] Banner appears when payment pending
- [ ] Banner shows on all dashboard pages
- [ ] Banner has correct styling and animation
- [ ] Banner disappears after verification

### Admin Verification ✅
- [ ] Admin can see pending payments
- [ ] Admin can view payment proof
- [ ] Admin can verify payment
- [ ] User access updated automatically
- [ ] Verification details recorded

---

## Test URLs

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Payment Page**: http://127.0.0.1:8000/payment/ (requires login)
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (requires login)
- **All Profiles**: http://127.0.0.1:8000/dashboard/ (requires login)
- **My Profile**: http://127.0.0.1:8000/dashboard/my_profile/ (requires login)

---

## Common Issues & Solutions

### OTP Not Sending
- Check Firebase billing enabled
- Check Phone Authentication enabled
- Check reCAPTCHA configuration
- Check rate limits

### Payment Banner Not Showing
- Check `payment_done = False` in database
- Check payment transaction exists
- Check context processor is loaded
- Clear browser cache

### Admin Can't See Payments
- Check admin user is superuser
- Check payment status is 'pending'
- Check admin_notified flag
- Refresh admin page

---

## Success Criteria

✅ All tests pass
✅ No errors in browser console
✅ No errors in Django logs
✅ Payment workflow complete
✅ Admin verification works
✅ Banner appears/disappears correctly

**Website is ready for production!** 🚀

