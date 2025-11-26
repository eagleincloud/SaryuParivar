#!/usr/bin/env python
"""
Test boto3 S3 integration
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.s3_utils import (
    get_s3_client,
    get_s3_object,
    check_s3_object_exists,
    serve_s3_image
)
from Saryupari_Brahmin_Project.settings import AWS_STORAGE_BUCKET_NAME
from administration.models import CustomUser
from django.test import RequestFactory

def test_s3_client():
    """Test S3 client creation"""
    print("=" * 60)
    print("1. Testing S3 Client Creation")
    print("=" * 60)
    
    client = get_s3_client()
    if client:
        print("✅ S3 client created successfully")
        return True
    else:
        print("❌ Failed to create S3 client")
        return False

def test_s3_object_exists():
    """Test checking if object exists"""
    print("\n" + "=" * 60)
    print("2. Testing S3 Object Existence Check")
    print("=" * 60)
    
    # Get a sample file path from database
    user = CustomUser.objects.exclude(profile_pic='').first()
    if not user or not user.profile_pic:
        print("⚠️  No user with profile pic found")
        return None
    
    file_path = user.profile_pic.name  # This is the S3 key
    print(f"Testing file: {file_path}")
    
    exists = check_s3_object_exists(AWS_STORAGE_BUCKET_NAME, file_path)
    if exists:
        print(f"✅ File exists in S3: {file_path}")
        return True
    else:
        print(f"⚠️  File not found or not accessible: {file_path}")
        return False

def test_get_s3_object():
    """Test fetching object from S3"""
    print("\n" + "=" * 60)
    print("3. Testing Fetch Object from S3")
    print("=" * 60)
    
    user = CustomUser.objects.exclude(profile_pic='').first()
    if not user or not user.profile_pic:
        print("⚠️  No user with profile pic found")
        return None
    
    file_path = user.profile_pic.name
    print(f"Fetching: {file_path}")
    
    content, content_type = get_s3_object(AWS_STORAGE_BUCKET_NAME, file_path)
    
    if content:
        print(f"✅ Successfully fetched object")
        print(f"   Size: {len(content)} bytes")
        print(f"   Content-Type: {content_type}")
        return True
    else:
        print(f"❌ Failed to fetch object")
        return False

def test_serve_s3_image():
    """Test serving image through Django view"""
    print("\n" + "=" * 60)
    print("4. Testing Serve S3 Image View")
    print("=" * 60)
    
    user = CustomUser.objects.exclude(profile_pic='').first()
    if not user or not user.profile_pic:
        print("⚠️  No user with profile pic found")
        return None
    
    # Extract file path (remove 'media/' prefix if present)
    file_path = user.profile_pic.name
    if file_path.startswith('media/'):
        file_path = file_path[6:]  # Remove 'media/' prefix
    
    print(f"Serving: {file_path}")
    
    factory = RequestFactory()
    request = factory.get(f'/media/{file_path}')
    
    try:
        response = serve_s3_image(request, file_path)
        if response.status_code == 200:
            print(f"✅ Successfully served image")
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.get('Content-Type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Failed to serve image: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error serving image: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("BOTO3 S3 INTEGRATION TEST")
    print("=" * 60)
    
    results = {}
    
    results['client'] = test_s3_client()
    results['exists'] = test_s3_object_exists()
    results['fetch'] = test_get_s3_object()
    results['serve'] = test_serve_s3_image()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"S3 Client: {'✅ PASS' if results['client'] else '❌ FAIL'}")
    exists_status = '✅ PASS' if results['exists'] is True else ('⚠️  SKIPPED' if results['exists'] is None else '❌ FAIL')
    print(f"Object Exists: {exists_status}")
    fetch_status = '✅ PASS' if results['fetch'] is True else ('⚠️  SKIPPED' if results['fetch'] is None else '❌ FAIL')
    print(f"Fetch Object: {fetch_status}")
    serve_status = '✅ PASS' if results['serve'] is True else ('⚠️  SKIPPED' if results['serve'] is None else '❌ FAIL')
    print(f"Serve Image: {serve_status}")
    
    all_passed = all(r for r in results.values() if r is not None)
    
    if all_passed:
        print("\n🎉 All boto3 S3 tests passed!")
        print("✅ Images can now be served through Django using boto3")
    else:
        print("\n⚠️  Some tests had issues")
        if results['client']:
            print("✅ S3 client works - core functionality should be fine")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

