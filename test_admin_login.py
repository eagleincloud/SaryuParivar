#!/usr/bin/env python
"""
Test Admin Login Script
Verifies admin credentials and provides login instructions
"""
import os
import sys
import django
from django.test import Client

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("ADMIN LOGIN TEST")
print("=" * 60)

# Check admin user
admin = User.objects.filter(is_superuser=True, username='admin').first()

if admin:
    print("\n✅ Admin User Found:")
    print(f"   Username: {admin.username}")
    print(f"   Email: {admin.email}")
    print(f"   Is Superuser: {admin.is_superuser}")
    print(f"   Is Staff: {admin.is_staff}")
    
    # Test login
    client = Client()
    login_success = client.login(username='admin', password='admin123')
    
    if login_success:
        print("\n✅ Login Test: SUCCESS")
        print("   Credentials are working!")
    else:
        print("\n⚠️  Login Test: FAILED")
        print("   Password may have been changed")
        print("   Current password: admin123")
else:
    print("\n⚠️  Admin user not found")
    print("   Creating admin user...")
    
    admin = User.objects.create_user(
        username='admin',
        email='admin@saryuparivar.com',
        password='admin123',
        is_superuser=True,
        is_staff=True
    )
    print("   ✅ Admin user created")

print("\n" + "=" * 60)
print("ADMIN LOGIN INSTRUCTIONS")
print("=" * 60)

print("""
1. Open browser: http://127.0.0.1:8000/admin/

2. Enter credentials:
   Username: admin
   Password: admin123

3. Click "Log in"

4. After login:
   - Go to: Users → Custom Users
   - Find user "admin"
   - Click to edit
   - Scroll to password section
   - Enter new password
   - Save

5. Test admin features:
   - Go to: Administration → Payment Transactions
   - View pending payments
   - Verify/reject payments
""")

print("\n" + "=" * 60)
print("ADMIN PANEL URLS")
print("=" * 60)
print("""
Main Admin: http://127.0.0.1:8000/admin/
Payment Transactions: http://127.0.0.1:8000/admin/administration/paymenttransaction/
Users: http://127.0.0.1:8000/admin/administration/customuser/
OTP Counters: http://127.0.0.1:8000/admin/administration/otprequestcounter/
""")

print("\n" + "=" * 60)
print("✅ Admin credentials ready!")
print("=" * 60)

