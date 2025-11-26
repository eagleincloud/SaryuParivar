# Login Credentials

## 🔐 Admin Credentials

**URL**: http://127.0.0.1:8000/admin/

**Username**: `admin`
**Password**: `admin123`
**Email**: admin@saryuparivar.com

⚠️ **IMPORTANT**: Change password after first login!

### To Change Admin Password:
1. Login to admin panel
2. Go to: Users → Custom Users
3. Find user "admin"
4. Click to edit
5. Change password
6. Save

---

## 👤 Platform User Credentials

### Login via OTP (Phone Number)

**URL**: http://127.0.0.1:8000/

**Available Test Users** (Phone Numbers):
- `9898998988` - aditya tiwari
- `9168591360` - Aditay asas
- `9753148000` - gautam tiwari
- `9167197348` - Test User
- `9227060715` - Test User

### How to Login:
1. Go to homepage: http://127.0.0.1:8000/
2. Click "Login" button
3. Enter phone number (10 digits, e.g., `9898998988`)
4. Click "Request OTP"
5. Enter OTP received via SMS
6. Click "Verify OTP"
7. You'll be logged in and redirected to dashboard

---

## ⚠️ OTP Not Working?

If you're not receiving OTP messages, check:

1. **Firebase Billing** (MOST COMMON ISSUE):
   - Go to: https://console.firebase.google.com/
   - Project: saryuparivar-acc39
   - Settings → Usage and billing
   - Upgrade to Blaze plan
   - Add payment method

2. **Phone Authentication Enabled**:
   - Firebase Console → Authentication → Sign-in method
   - Enable "Phone" provider

3. **Check Browser Console**:
   - Press F12 → Console tab
   - Look for error messages
   - Common: `auth/billing-not-enabled`

See `OTP_TROUBLESHOOTING.md` for detailed troubleshooting.

---

## 🧪 Testing Without SMS

### Use Firebase Test Phone Numbers:

1. **Add Test Number in Firebase**:
   - Go to Firebase Console
   - Authentication → Sign-in method → Phone
   - Scroll to "Phone numbers for testing"
   - Add: `+919898998988` with code: `123456`

2. **Use in App**:
   - Enter phone: `9898998988`
   - Click "Request OTP"
   - Enter test code: `123456`
   - No actual SMS sent

---

## 📋 Quick Access

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (requires login)
- **Payment Page**: http://127.0.0.1:8000/payment/ (requires login)

---

## 🔒 Security Notes

1. **Change Admin Password**: Immediately after first login
2. **Use Strong Passwords**: For production
3. **Enable 2FA**: Recommended for admin accounts
4. **Test Users**: These are for development only

---

## 📞 Support

If login issues persist:
1. Check `OTP_TROUBLESHOOTING.md` for OTP issues
2. Verify Firebase billing is enabled
3. Check browser console for errors
4. Verify Phone Authentication is enabled in Firebase

