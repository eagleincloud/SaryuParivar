# Quick Start Guide

## 🔐 Login Credentials

### Admin Panel
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`
- ⚠️ **Change password after first login!**

### Platform Users (OTP Login)
- **URL**: http://127.0.0.1:8000/
- **Method**: Phone number + OTP
- **Test Phone Numbers**:
  - `9898998988` - aditya tiwari
  - `9168591360` - Aditay asas
  - `9753148000` - gautam tiwari

---

## ⚠️ OTP Not Working? (Most Common Issue)

### Problem: Not receiving SMS messages

**Solution**: Enable Firebase Billing (REQUIRED)

1. **Go to Firebase Console**:
   - https://console.firebase.google.com/
   - Select project: **saryuparivar-acc39**

2. **Enable Billing**:
   - Click **⚙️ Project Settings**
   - Go to **Usage and billing** tab
   - Click **Upgrade to Blaze plan**
   - Add payment method (credit/debit card)
   - Wait 1-2 minutes for activation

3. **Enable Phone Authentication**:
   - Go to **Authentication** → **Sign-in method**
   - Find **Phone** in the list
   - Click **Phone** → Toggle **Enable** to ON
   - Click **Save**

4. **Test Again**:
   - Go to: http://127.0.0.1:8000/
   - Click "Login"
   - Enter phone number
   - Click "Request OTP"
   - You should receive SMS

---

## 🧪 Test Without SMS (Development)

### Use Firebase Test Phone Numbers:

1. **Add Test Number**:
   - Firebase Console → Authentication → Sign-in method → Phone
   - Scroll to "Phone numbers for testing"
   - Add: `+919898998988` with code: `123456`

2. **Use in App**:
   - Enter phone: `9898998988`
   - Click "Request OTP"
   - Enter test code: `123456`
   - No actual SMS sent!

---

## 📋 Quick Checklist

### For OTP to Work:
- [ ] Firebase billing enabled (Blaze plan)
- [ ] Phone Authentication enabled
- [ ] Phone number format correct (10 digits)
- [ ] Not rate limited (wait if needed)

### For Admin Access:
- [ ] Login at: http://127.0.0.1:8000/admin/
- [ ] Username: `admin`
- [ ] Password: `admin123`

---

## 🔍 Troubleshooting

### Check Browser Console:
1. Press **F12** (Developer Tools)
2. Go to **Console** tab
3. Try sending OTP
4. Look for error messages:
   - `auth/billing-not-enabled` → Enable billing
   - `auth/configuration-not-found` → Enable Phone Auth
   - `auth/too-many-requests` → Wait and retry

### Common Errors:

| Error | Solution |
|-------|----------|
| `auth/billing-not-enabled` | Enable billing in Firebase Console |
| `auth/configuration-not-found` | Enable Phone Authentication |
| `auth/too-many-requests` | Wait 5-10 minutes |
| `auth/invalid-phone-number` | Use 10 digits only |

---

## 📞 Need Help?

1. **Check**: `OTP_TROUBLESHOOTING.md` for detailed guide
2. **Check**: Browser console (F12) for errors
3. **Verify**: Firebase billing is enabled
4. **Verify**: Phone Authentication is enabled

---

## ✅ Quick Test

1. **Admin Login**:
   ```
   URL: http://127.0.0.1:8000/admin/
   Username: admin
   Password: admin123
   ```

2. **User Login (OTP)**:
   ```
   URL: http://127.0.0.1:8000/
   Phone: 9898998988
   OTP: (from SMS or test code: 123456)
   ```

---

## 🚀 Ready to Use!

- ✅ Admin credentials created
- ✅ Platform users available
- ⚠️ OTP requires Firebase billing enabled
- 📖 See `CREDENTIALS.md` for all credentials
- 📖 See `OTP_TROUBLESHOOTING.md` for OTP help

