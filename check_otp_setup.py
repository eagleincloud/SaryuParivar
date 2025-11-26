#!/usr/bin/env python
"""
Quick OTP Setup Checker
Checks Firebase configuration and common issues
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.firebase_config import FIREBASE_CONFIG

print("=" * 60)
print("OTP SETUP DIAGNOSTIC")
print("=" * 60)

print("\n✅ Firebase Configuration:")
print(f"   Project ID: {FIREBASE_CONFIG['projectId']}")
print(f"   Auth Domain: {FIREBASE_CONFIG['authDomain']}")
print(f"   API Key: {FIREBASE_CONFIG['apiKey'][:20]}...")

print("\n⚠️  COMMON OTP ISSUES:")
print("\n1. Firebase Billing Not Enabled (MOST COMMON)")
print("   → Go to: https://console.firebase.google.com/")
print("   → Project: saryuparivar-acc39")
print("   → Settings → Usage and billing")
print("   → Upgrade to Blaze plan")
print("   → Add payment method")

print("\n2. Phone Authentication Not Enabled")
print("   → Firebase Console → Authentication → Sign-in method")
print("   → Enable 'Phone' provider")

print("\n3. Rate Limiting")
print("   → Wait 5-10 minutes between requests")
print("   → Use different phone number for testing")

print("\n4. Invalid Phone Format")
print("   → Enter 10 digits only (e.g., 9898998988)")
print("   → App adds +91 automatically")

print("\n📋 QUICK FIX STEPS:")
print("   1. Enable Billing: Firebase Console → Settings → Usage and billing")
print("   2. Enable Phone Auth: Authentication → Sign-in method → Phone")
print("   3. Test with test number (no SMS needed)")
print("   4. Check browser console (F12) for errors")

print("\n🧪 TEST WITHOUT SMS:")
print("   1. Firebase Console → Authentication → Sign-in method → Phone")
print("   2. Add test number: +919898998988 with code: 123456")
print("   3. Use phone: 9898998988 in app")
print("   4. Enter test code: 123456")

print("\n" + "=" * 60)
print("See OTP_TROUBLESHOOTING.md for detailed guide")
print("=" * 60)

