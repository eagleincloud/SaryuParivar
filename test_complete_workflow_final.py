#!/usr/bin/env python
"""
Complete Workflow Test
Tests: Registration → Payment → OTP Login → Admin Verification → Banner
"""
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import CustomUser, PaymentTransaction
from django.contrib.auth import get_user_model

print("=" * 60)
print("COMPLETE WORKFLOW TEST")
print("=" * 60)
print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "=" * 60)
print("WORKFLOW STEPS")
print("=" * 60)

print("\n📝 STEP 1: REGISTRATION & PAYMENT")
print("""
1. Go to: http://127.0.0.1:8000/
2. Click "Register"
3. Fill registration form:
   - Name, Surname, Father's Name
   - Phone: 10 digits
   - Address details
4. Submit form
5. ✅ Payment modal should appear
6. Upload payment proof (screenshot)
7. Click "Submit Payment Proof"
8. ✅ Success message: "Payment proof uploaded successfully"
""")

print("\n📱 STEP 2: OTP LOGIN")
print("""
1. Go to: http://127.0.0.1:8000/
2. Click "Login"
3. Enter registered phone number
4. Click "Request OTP"
5. ✅ Check browser console (F12):
   - If error: Follow OTP troubleshooting
   - If success: "OTP sent successfully!"
6. Enter OTP from SMS (or test code: 123456)
7. Click "Verify OTP"
8. ✅ Should redirect to /dashboard/
9. ✅ Payment banner should appear at top
""")

print("\n👨‍💼 STEP 3: ADMIN VERIFICATION")
print("""
1. Login as admin: http://127.0.0.1:8000/admin/
   Username: admin
   Password: admin123

2. Go to: Administration → Payment Transactions

3. Find pending payment:
   - Look for "⚠️ NEW - Needs Review"
   - Or status: "Pending Verification"

4. Click payment to view:
   - User details
   - Transaction ID
   - Payment proof (if uploaded)
   - Amount

5. Verify payment:
   - Change "Payment status" to "Completed"
   - Optionally add remarks
   - Click "Save"

6. ✅ Success message: "Payment verified successfully"
7. ✅ User.payment_done = True (automatic)
""")

print("\n🎯 STEP 4: BANNER REMOVAL")
print("""
1. User logs out
2. User logs in again via OTP
3. Go to dashboard
4. ✅ Payment banner should NOT appear
5. ✅ Full access to all features
""")

print("\n" + "=" * 60)
print("CURRENT STATUS CHECK")
print("=" * 60)

# Check users
users = CustomUser.objects.exclude(is_superuser=True)
pending_users = users.filter(payment_done=False)
verified_users = users.filter(payment_done=True)

print(f"\n📊 Users:")
print(f"   Total: {users.count()}")
print(f"   Pending Payment: {pending_users.count()}")
print(f"   Verified Payment: {verified_users.count()}")

# Check payments
payments = PaymentTransaction.objects.all()
pending_payments = payments.filter(payment_status='pending')
completed_payments = payments.filter(payment_status='completed')

print(f"\n💳 Payments:")
print(f"   Total: {payments.count()}")
print(f"   Pending: {pending_payments.count()}")
print(f"   Completed: {completed_payments.count()}")

# Sample pending payment
if pending_payments.exists():
    payment = pending_payments.first()
    print(f"\n📋 Sample Pending Payment:")
    print(f"   User: {payment.user.show_username()}")
    print(f"   Transaction: {payment.transaction_id}")
    print(f"   Amount: ₹{payment.amount}")
    print(f"   Has Proof: {'Yes' if payment.payment_proof else 'No'}")
    print(f"   Admin Notified: {payment.admin_notified}")

print("\n" + "=" * 60)
print("TESTING CHECKLIST")
print("=" * 60)

print("""
[ ] 1. Registration creates payment transaction
[ ] 2. Payment modal appears after registration
[ ] 3. Payment proof uploads successfully
[ ] 4. OTP sends successfully (check SMS or test code)
[ ] 5. OTP verification works
[ ] 6. User logged in successfully
[ ] 7. Payment banner appears on dashboard
[ ] 8. Admin can see pending payments
[ ] 9. Admin can verify payment
[ ] 10. User access updated automatically
[ ] 11. Banner removed after verification
[ ] 12. Full access granted
""")

print("\n" + "=" * 60)
print("QUICK TEST URLS")
print("=" * 60)
print("""
Homepage: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/
Dashboard: http://127.0.0.1:8000/dashboard/
Payment: http://127.0.0.1:8000/payment/
""")

print("\n" + "=" * 60)
print("✅ Ready to test complete workflow!")
print("=" * 60)

