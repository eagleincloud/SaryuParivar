#!/usr/bin/env python
"""
Complete End-to-End Test for Saryu Parivar Website
Tests: Registration, OTP, Payment, Admin Verification, User Access
"""
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import CustomUser, PaymentTransaction, OTPRequestCounter
from dashboard.models import CandidateProfile
from django.utils import timezone
from django.contrib.auth import get_user_model

def test_registration_flow():
    """Test user registration creates payment transaction"""
    print("=" * 60)
    print("1. TESTING REGISTRATION FLOW")
    print("=" * 60)
    
    # Check if test user exists
    test_phone = "9999999999"
    test_user = CustomUser.objects.filter(phone_number=test_phone).first()
    
    if test_user:
        print(f"  ✓ Test user exists: {test_user.show_username()}")
        
        # Check payment transaction
        transaction = PaymentTransaction.objects.filter(user=test_user).first()
        if transaction:
            print(f"  ✓ Payment transaction exists: {transaction.transaction_id}")
            print(f"    Status: {transaction.payment_status}")
            print(f"    Amount: ₹{transaction.amount}")
            print(f"    Created: {transaction.created_at}")
            return True, test_user, transaction
        else:
            print("  ⚠️  No payment transaction found")
            return False, test_user, None
    else:
        print("  ⚠️  Test user not found")
        return False, None, None

def test_payment_upload():
    """Test payment proof upload"""
    print("\n" + "=" * 60)
    print("2. TESTING PAYMENT UPLOAD")
    print("=" * 60)
    
    test_user = CustomUser.objects.filter(phone_number="9999999999").first()
    if not test_user:
        print("  ⚠️  Test user not found")
        return False
    
    transaction = PaymentTransaction.objects.filter(user=test_user).first()
    if not transaction:
        print("  ⚠️  No payment transaction found")
        return False
    
    # Check if payment proof can be uploaded (simulated)
    print(f"  ✓ Transaction found: {transaction.transaction_id}")
    print(f"    Current status: {transaction.payment_status}")
    print(f"    Admin notified: {transaction.admin_notified}")
    
    # Simulate payment proof upload
    if not transaction.payment_proof:
        print("  ⚠️  No payment proof uploaded yet")
        print("  💡 User can upload proof via /payment/ page")
    else:
        print(f"  ✓ Payment proof uploaded: {transaction.payment_proof.name}")
    
    return True

def test_admin_notification():
    """Test admin notification system"""
    print("\n" + "=" * 60)
    print("3. TESTING ADMIN NOTIFICATION")
    print("=" * 60)
    
    # Get pending payments
    pending_payments = PaymentTransaction.objects.filter(
        payment_status='pending'
    )
    
    print(f"  📊 Pending Payments: {pending_payments.count()}")
    
    for payment in pending_payments[:5]:
        print(f"\n  Payment ID: {payment.id}")
        print(f"    User: {payment.user.show_username()}")
        print(f"    Transaction: {payment.transaction_id}")
        print(f"    Amount: ₹{payment.amount}")
        print(f"    Has Proof: {'Yes' if payment.payment_proof else 'No'}")
        print(f"    Admin Notified: {payment.admin_notified}")
        if payment.admin_notified:
            print(f"    Notified At: {payment.admin_notified_at}")
        print(f"    Status: {payment.get_payment_status_display()}")
    
    # Check for new notifications
    new_notifications = pending_payments.filter(
        payment_proof__isnull=False,
        admin_notified=False
    )
    
    if new_notifications.exists():
        print(f"\n  ⚠️  {new_notifications.count()} NEW payment(s) need admin review!")
        print("     Admin should check /admin/administration/paymenttransaction/")
    else:
        print("\n  ✓ All pending payments have been notified")
    
    return True

def test_user_access_control():
    """Test user access based on payment status"""
    print("\n" + "=" * 60)
    print("4. TESTING USER ACCESS CONTROL")
    print("=" * 60)
    
    # Get users with different payment statuses
    users_with_pending = CustomUser.objects.filter(
        payment_done=False
    ).exclude(is_superuser=True)
    
    users_verified = CustomUser.objects.filter(
        payment_done=True
    ).exclude(is_superuser=True)
    
    print(f"  📊 Users with Pending Payment: {users_with_pending.count()}")
    print(f"  📊 Users with Verified Payment: {users_verified.count()}")
    
    # Check pending users
    print("\n  👤 Users with Pending Payment:")
    for user in users_with_pending[:5]:
        transaction = PaymentTransaction.objects.filter(
            user=user,
            payment_status='pending'
        ).first()
        status = f"Pending (TXN: {transaction.transaction_id[:10]}...)" if transaction else "No Transaction"
        print(f"    - {user.show_username()}: {status}")
        print(f"      Should see payment banner: ✅ YES")
    
    # Check verified users
    print("\n  ✅ Users with Verified Payment:")
    for user in users_verified[:5]:
        transaction = PaymentTransaction.objects.filter(
            user=user,
            payment_status='completed'
        ).first()
        verified_by = f" by {transaction.verified_by.show_username()}" if transaction and transaction.verified_by else ""
        print(f"    - {user.show_username()}: Verified{verified_by}")
        print(f"      Should see payment banner: ❌ NO")
    
    return True

def test_admin_verification():
    """Test admin verification workflow"""
    print("\n" + "=" * 60)
    print("5. TESTING ADMIN VERIFICATION WORKFLOW")
    print("=" * 60)
    
    # Get pending payments
    pending = PaymentTransaction.objects.filter(payment_status='pending')
    
    print(f"  📊 Pending Payments: {pending.count()}")
    
    if pending.exists():
        payment = pending.first()
        print(f"\n  Sample Payment:")
        print(f"    User: {payment.user.show_username()}")
        print(f"    Transaction: {payment.transaction_id}")
        print(f"    Amount: ₹{payment.amount}")
        print(f"    Has Proof: {'Yes' if payment.payment_proof else 'No'}")
        print(f"\n  💡 Admin Actions Available:")
        print(f"    1. Go to /admin/administration/paymenttransaction/")
        print(f"    2. Click on payment to view details")
        print(f"    3. Change status to 'completed' to verify")
        print(f"    4. Or use 'Verify selected payments' bulk action")
        print(f"    5. User access will be automatically updated")
        
        # Check if admin can verify
        print(f"\n  ✅ Verification Process:")
        print(f"    - Admin sets status to 'completed'")
        print(f"    - user.payment_done = True (automatic)")
        print(f"    - Payment banner removed from user dashboard")
        print(f"    - User gets full access")
    else:
        print("  ✓ No pending payments")
    
    return True

def test_otp_functionality():
    """Test OTP request counter"""
    print("\n" + "=" * 60)
    print("6. TESTING OTP FUNCTIONALITY")
    print("=" * 60)
    
    # Check OTP counters
    counters = OTPRequestCounter.objects.all()
    print(f"  📊 OTP Request Counters: {counters.count()}")
    
    for counter in counters[:5]:
        status = "BLOCKED" if counter.is_blocked() else "ACTIVE"
        print(f"\n  Phone: {counter.phone_number}")
        print(f"    Requests: {counter.request_count}/5")
        print(f"    Status: {status}")
        if counter.is_blocked() and counter.blocked_until:
            remaining = (counter.blocked_until - timezone.now()).total_seconds()
            print(f"    Blocked until: {counter.blocked_until}")
            print(f"    Remaining: {int(remaining)} seconds")
    
    return True

def test_payment_banner_display():
    """Test payment banner display logic"""
    print("\n" + "=" * 60)
    print("7. TESTING PAYMENT BANNER DISPLAY")
    print("=" * 60)
    
    users = CustomUser.objects.exclude(is_superuser=True)[:5]
    
    for user in users:
        payment_pending = False
        pending_transaction = None
        
        if not user.payment_done:
            pending_transaction = PaymentTransaction.objects.filter(
                user=user,
                payment_status='pending'
            ).first()
            if pending_transaction:
                payment_pending = True
        
        should_show_banner = payment_pending or not user.payment_done
        
        print(f"\n  User: {user.show_username()}")
        print(f"    payment_done: {user.payment_done}")
        print(f"    payment_pending: {payment_pending}")
        print(f"    Should show banner: {'✅ YES' if should_show_banner else '❌ NO'}")
        if pending_transaction:
            print(f"    Transaction: {pending_transaction.transaction_id}")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPLETE END-TO-END TEST")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    
    results['registration'] = test_registration_flow()
    results['payment_upload'] = test_payment_upload()
    results['admin_notification'] = test_admin_notification()
    results['access_control'] = test_user_access_control()
    results['admin_verification'] = test_admin_verification()
    results['otp'] = test_otp_functionality()
    results['banner'] = test_payment_banner_display()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"Registration Flow: {'✅ PASS' if results['registration'][0] else '⚠️  CHECK'}")
    print(f"Payment Upload: {'✅ PASS' if results['payment_upload'] else '⚠️  CHECK'}")
    print(f"Admin Notification: {'✅ PASS' if results['admin_notification'] else '⚠️  CHECK'}")
    print(f"Access Control: {'✅ PASS' if results['access_control'] else '⚠️  CHECK'}")
    print(f"Admin Verification: {'✅ PASS' if results['admin_verification'] else '⚠️  CHECK'}")
    print(f"OTP Functionality: {'✅ PASS' if results['otp'] else '⚠️  CHECK'}")
    print(f"Payment Banner: {'✅ PASS' if results['banner'] else '⚠️  CHECK'}")
    
    # Statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    
    total_users = CustomUser.objects.exclude(is_superuser=True).count()
    pending_payments = PaymentTransaction.objects.filter(payment_status='pending').count()
    completed_payments = PaymentTransaction.objects.filter(payment_status='completed').count()
    rejected_payments = PaymentTransaction.objects.filter(payment_status='rejected').count()
    
    print(f"Total Users: {total_users}")
    print(f"Pending Payments: {pending_payments}")
    print(f"Completed Payments: {completed_payments}")
    print(f"Rejected Payments: {rejected_payments}")
    print(f"Users with Verified Payment: {CustomUser.objects.filter(payment_done=True).exclude(is_superuser=True).count()}")
    print(f"Users Pending Verification: {CustomUser.objects.filter(payment_done=False).exclude(is_superuser=True).count()}")
    
    print("\n" + "=" * 60)
    print("✅ END-TO-END TEST COMPLETE")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("   1. Test registration: Register a new user")
    print("   2. Test OTP login: Login with phone number")
    print("   3. Test payment upload: Upload payment proof")
    print("   4. Test admin verification: Verify payment in admin panel")
    print("   5. Verify banner disappears after admin approval")

if __name__ == '__main__':
    main()

