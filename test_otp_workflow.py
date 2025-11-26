#!/usr/bin/env python
"""
Test OTP Workflow Script
Tests OTP functionality after Firebase setup
"""
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import CustomUser, OTPRequestCounter
from Saryupari_Brahmin_Project.firebase_config import FIREBASE_CONFIG

print("=" * 60)
print("OTP WORKFLOW TEST")
print("=" * 60)
print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n✅ Firebase Configuration:")
print(f"   Project ID: {FIREBASE_CONFIG['projectId']}")
print(f"   Auth Domain: {FIREBASE_CONFIG['authDomain']}")

print("\n" + "=" * 60)
print("TEST USERS AVAILABLE")
print("=" * 60)

users = CustomUser.objects.exclude(is_superuser=True)[:5]
for i, user in enumerate(users, 1):
    print(f"\n{i}. Phone: {user.phone_number}")
    print(f"   Name: {user.show_username()}")
    print(f"   Username: {user.username}")

print("\n" + "=" * 60)
print("TESTING INSTRUCTIONS")
print("=" * 60)

print("\n📱 TEST 1: OTP with Real SMS")
print("""
1. Open browser: http://127.0.0.1:8000/
2. Click "Login" button
3. Enter phone number (e.g., 9898998988)
4. Click "Request OTP"
5. Check browser console (F12) for errors:
   - If error: auth/billing-not-enabled → Enable billing
   - If error: auth/configuration-not-found → Enable Phone Auth
   - If success: "OTP sent successfully!"
6. Check phone for SMS with 6-digit code
7. Enter OTP code
8. Click "Verify OTP"
9. Should redirect to /dashboard/
""")

print("\n🧪 TEST 2: OTP with Test Number (No SMS)")
print("""
1. First, add test number in Firebase Console:
   - Authentication → Sign-in method → Phone
   - Scroll to "Phone numbers for testing"
   - Add: +919898998988 with code: 123456

2. In application:
   - Enter phone: 9898998988
   - Click "Request OTP"
   - Enter test code: 123456
   - Click "Verify OTP"
   - Should login successfully
""")

print("\n" + "=" * 60)
print("RATE LIMITING CHECK")
print("=" * 60)

test_phone = "9898998988"
counter = OTPRequestCounter.get_or_create_counter(test_phone)

print(f"\nPhone: {test_phone}")
print(f"Requests: {counter.request_count}/5")
print(f"Remaining: {counter.get_remaining_requests(max_requests=5)}")
print(f"Status: {'🔴 BLOCKED' if counter.is_blocked() else '🟢 ACTIVE'}")

if counter.is_blocked():
    from django.utils import timezone
    remaining = (counter.blocked_until - timezone.now()).total_seconds()
    print(f"Blocked until: {counter.blocked_until}")
    print(f"Time remaining: {int(remaining)} seconds")
    print("\n⚠️  Rate limit reached. Wait before testing.")

print("\n" + "=" * 60)
print("BROWSER CONSOLE CHECK")
print("=" * 60)
print("""
When testing OTP, check browser console (F12):

✅ SUCCESS:
   - "Firebase initialized successfully"
   - "reCAPTCHA verified"
   - "OTP sent successfully!"

❌ ERRORS:
   - auth/billing-not-enabled → Enable billing
   - auth/configuration-not-found → Enable Phone Auth
   - auth/too-many-requests → Wait and retry
   - auth/invalid-phone-number → Check format
""")

print("\n" + "=" * 60)
print("QUICK TEST COMMANDS")
print("=" * 60)
print("""
1. Start server:
   python manage.py runserver

2. Open browser:
   http://127.0.0.1:8000/

3. Test OTP:
   - Click Login
   - Enter phone: 9898998988
   - Request OTP
   - Enter code from SMS or test code: 123456

4. Check console:
   - Press F12
   - Check Console tab for errors
""")

print("\n" + "=" * 60)
print("✅ Ready to test!")
print("=" * 60)

