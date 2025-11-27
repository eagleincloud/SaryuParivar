#!/usr/bin/env python
"""
Test script to verify that user_profile and shortlisted_profiles views
render the correct templates and don't redirect to all_profiles.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from dashboard import views

User = get_user_model()
factory = RequestFactory()

# Get a test user
try:
    user = User.objects.filter(is_superuser=False).first()
    if not user:
        print("❌ No non-admin users found. Please create a test user first.")
        exit(1)
    
    print(f"Testing with user: {user.username}")
    print("=" * 60)
    
    # Test user_profile view
    print("\n1. Testing user_profile view:")
    print("-" * 60)
    request = factory.get('/dashboard/user_profile/')
    request.user = user
    
    try:
        response = views.user_profile(request)
        print(f"   Status Code: {response.status_code}")
        print(f"   Template Used: {response.template_name if hasattr(response, 'template_name') else 'N/A'}")
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            if 'MY PROFILE - EDIT YOUR INFORMATION' in content:
                print("   ✅ Correct template content found (Orange banner)")
            elif 'all-profiles' in content.lower() or 'Browse Profiles' in content:
                print("   ❌ WRONG! All profiles page content found!")
            else:
                print("   ⚠️  Template content unclear")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test shortlisted_profiles view
    print("\n2. Testing shortlisted_profiles view:")
    print("-" * 60)
    request = factory.get('/dashboard/shortlisted_profiles/')
    request.user = user
    
    try:
        response = views.shortlisted_profiles(request)
        print(f"   Status Code: {response.status_code}")
        print(f"   Template Used: {response.template_name if hasattr(response, 'template_name') else 'N/A'}")
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            if 'MY SHORTLISTED PROFILES - VIEW YOUR FAVORITES' in content:
                print("   ✅ Correct template content found (Blue banner)")
            elif 'all-profiles' in content.lower() or 'Browse Profiles' in content:
                print("   ❌ WRONG! All profiles page content found!")
            else:
                print("   ⚠️  Template content unclear")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test all_profiles view for comparison
    print("\n3. Testing all_profiles view (for comparison):")
    print("-" * 60)
    request = factory.get('/dashboard/')
    request.user = user
    
    try:
        response = views.all_profiles(request)
        print(f"   Status Code: {response.status_code}")
        print(f"   Template Used: {response.template_name if hasattr(response, 'template_name') else 'N/A'}")
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            if 'all-profiles' in content.lower() or 'Browse Profiles' in content:
                print("   ✅ Correct template content found (All profiles page)")
            else:
                print("   ⚠️  Template content unclear")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

