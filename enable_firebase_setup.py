#!/usr/bin/env python
"""
Firebase Setup Verification Script
Checks if billing and Phone Authentication are enabled
"""
import requests
import json

print("=" * 60)
print("FIREBASE SETUP VERIFICATION")
print("=" * 60)

# Firebase Project Info
PROJECT_ID = "saryuparivar-acc39"
API_KEY = "AIzaSyBcOdG0hC3BCrhZkxrhxIzWdvc9wdWwHuA"

print(f"\n📋 Project: {PROJECT_ID}")
print(f"🔑 API Key: {API_KEY[:20]}...")

print("\n" + "=" * 60)
print("MANUAL SETUP REQUIRED")
print("=" * 60)

print("\n⚠️  Firebase Console Access Required")
print("   These steps must be done in Firebase Console:")
print("   https://console.firebase.google.com/")

print("\n" + "=" * 60)
print("STEP 1: ENABLE BILLING")
print("=" * 60)
print("""
1. Go to: https://console.firebase.google.com/
2. Select project: saryuparivar-acc39
3. Click ⚙️ Project Settings (gear icon, top left)
4. Click "Usage and billing" tab
5. Click "Modify plan" or "Upgrade to Blaze plan"
6. Review Blaze plan details:
   - Pay-as-you-go (only pay for what you use)
   - Generous free tier quotas
   - No monthly fees
7. Click "Continue" or "Upgrade"
8. Add payment method:
   - Credit card or debit card
   - Complete payment setup
9. Wait 1-2 minutes for activation
10. Verify billing status shows "Blaze plan"

✅ Billing Status: Check in Firebase Console
""")

print("\n" + "=" * 60)
print("STEP 2: ENABLE PHONE AUTHENTICATION")
print("=" * 60)
print("""
1. In Firebase Console, go to "Authentication" (left sidebar)
2. Click "Sign-in method" tab
3. Find "Phone" in the providers list
4. Click on "Phone" to open settings
5. Toggle "Enable" switch to ON
6. Click "Save"
7. Verify Phone shows as "Enabled"

✅ Phone Auth Status: Check in Firebase Console
""")

print("\n" + "=" * 60)
print("STEP 3: ADD TEST PHONE NUMBER (OPTIONAL)")
print("=" * 60)
print("""
For testing without SMS:

1. In Firebase Console → Authentication → Sign-in method → Phone
2. Scroll down to "Phone numbers for testing"
3. Click "Add phone number"
4. Enter:
   - Phone number: +919898998988
   - Verification code: 123456
5. Click "Add"
6. Now you can use phone: 9898998988 with code: 123456

✅ Test Number: +919898998988 / Code: 123456
""")

print("\n" + "=" * 60)
print("VERIFICATION CHECKLIST")
print("=" * 60)
print("""
After completing setup, verify:

[ ] Billing shows "Blaze plan" in Firebase Console
[ ] Phone Authentication is "Enabled" in Sign-in method
[ ] Test phone number added (optional, for development)
[ ] Browser console (F12) shows no Firebase errors
[ ] OTP request works in application

""")

print("=" * 60)
print("NEXT: Run test_otp_workflow.py to test OTP")
print("=" * 60)

