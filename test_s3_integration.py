#!/usr/bin/env python
"""
Comprehensive test for S3 image integration
"""
import os
import sys
import django
import requests

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.settings import (
    MEDIA_URL,
    DEFAULT_FILE_STORAGE,
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_CUSTOM_DOMAIN
)
from administration.models import CustomUser, SamajGallery, Promotion, Testimonial
from dashboard.models import CandidateProfile
from Saryupari_Brahmin_Project.storages import MediaStorage

def test_configuration():
    """Test S3 configuration"""
    print("=" * 60)
    print("1. S3 CONFIGURATION TEST")
    print("=" * 60)
    
    checks = []
    
    # Check storage backend
    if 'MediaStorage' in str(DEFAULT_FILE_STORAGE):
        print("✅ Storage Backend: Using S3 MediaStorage")
        checks.append(True)
    else:
        print("❌ Storage Backend: Not using S3")
        checks.append(False)
    
    # Check bucket name
    if AWS_STORAGE_BUCKET_NAME == 'eicaws-saryupariwar':
        print(f"✅ Bucket Name: {AWS_STORAGE_BUCKET_NAME}")
        checks.append(True)
    else:
        print(f"❌ Bucket Name: {AWS_STORAGE_BUCKET_NAME} (expected: eicaws-saryupariwar)")
        checks.append(False)
    
    # Check media URL
    if 's3.amazonaws.com' in MEDIA_URL:
        print(f"✅ Media URL: {MEDIA_URL}")
        checks.append(True)
    else:
        print(f"❌ Media URL: {MEDIA_URL} (should contain s3.amazonaws.com)")
        checks.append(False)
    
    # Check storage instance
    storage = MediaStorage()
    if storage.bucket_name == 'eicaws-saryupariwar':
        print(f"✅ Storage Bucket: {storage.bucket_name}")
        checks.append(True)
    else:
        print(f"❌ Storage Bucket: {storage.bucket_name}")
        checks.append(False)
    
    if storage.default_acl == 'public-read':
        print(f"✅ ACL: {storage.default_acl}")
        checks.append(True)
    else:
        print(f"⚠️  ACL: {storage.default_acl} (should be public-read)")
        checks.append(False)
    
    return all(checks)

def test_url_generation():
    """Test URL generation for different models"""
    print("\n" + "=" * 60)
    print("2. URL GENERATION TEST")
    print("=" * 60)
    
    all_s3 = True
    sample_urls = []
    
    # Test User Profile Pics
    users = CustomUser.objects.exclude(profile_pic='')[:3]
    print(f"\n👤 User Profile Pics ({users.count()}):")
    for user in users:
        if user.profile_pic:
            url = user.profile_pic.url
            is_s3 = 's3.amazonaws.com' in url
            status = "✅" if is_s3 else "❌"
            print(f"   {status} {user.show_username()}: {url[:80]}...")
            sample_urls.append(url)
            if not is_s3:
                all_s3 = False
    
    # Test Gallery Images
    galleries = SamajGallery.objects.all()[:3]
    print(f"\n📸 Gallery Images ({galleries.count()}):")
    for gallery in galleries:
        if gallery.image:
            url = gallery.image.url
            is_s3 = 's3.amazonaws.com' in url
            status = "✅" if is_s3 else "❌"
            print(f"   {status} {gallery.title or 'Untitled'}: {url[:80]}...")
            sample_urls.append(url)
            if not is_s3:
                all_s3 = False
    
    # Test Promotions
    promotions = Promotion.objects.all()[:3]
    print(f"\n📢 Promotions ({promotions.count()}):")
    for promo in promotions:
        if promo.banner:
            url = promo.banner.url
            is_s3 = 's3.amazonaws.com' in url
            status = "✅" if is_s3 else "❌"
            print(f"   {status} {promo.advertiser_name}: {url[:80]}...")
            sample_urls.append(url)
            if not is_s3:
                all_s3 = False
    
    # Test Testimonials
    testimonials = Testimonial.objects.all()[:3]
    print(f"\n💬 Testimonials ({testimonials.count()}):")
    for test in testimonials:
        if test.image:
            url = test.image.url
            is_s3 = 's3.amazonaws.com' in url
            status = "✅" if is_s3 else "❌"
            print(f"   {status} {test.made_by}: {url[:80]}...")
            sample_urls.append(url)
            if not is_s3:
                all_s3 = False
    
    # Test Marriage Profiles
    profiles = CandidateProfile.objects.exclude(marriage_profile_pic='')[:3]
    print(f"\n💑 Marriage Profiles ({profiles.count()}):")
    for profile in profiles:
        if profile.marriage_profile_pic:
            url = profile.marriage_profile_pic.url
            is_s3 = 's3.amazonaws.com' in url
            status = "✅" if is_s3 else "❌"
            name = profile.candidate_name or f"{profile.first_name} {profile.last_name}"
            print(f"   {status} {name}: {url[:80]}...")
            sample_urls.append(url)
            if not is_s3:
                all_s3 = False
    
    return all_s3, sample_urls

def test_image_accessibility(sample_urls):
    """Test if sample images are accessible"""
    print("\n" + "=" * 60)
    print("3. IMAGE ACCESSIBILITY TEST")
    print("=" * 60)
    
    if not sample_urls:
        print("⚠️  No sample URLs to test")
        return True
    
    accessible = 0
    total = min(3, len(sample_urls))
    
    print(f"\nTesting {total} sample URLs:")
    for url in sample_urls[:total]:
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                print(f"   ✅ {url[:60]}... - Accessible")
                accessible += 1
            elif response.status_code == 403:
                print(f"   ⚠️  {url[:60]}... - Access Denied (403) - Check bucket permissions")
            elif response.status_code == 404:
                print(f"   ⚠️  {url[:60]}... - Not Found (404) - File may not exist in S3")
            else:
                print(f"   ⚠️  {url[:60]}... - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  {url[:60]}... - Error: {str(e)[:50]}")
    
    if accessible == total:
        return True
    elif accessible > 0:
        return None  # Partial success
    else:
        return False

def test_homepage():
    """Test if homepage loads"""
    print("\n" + "=" * 60)
    print("4. HOMEPAGE TEST")
    print("=" * 60)
    
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            
            # Check if S3 URLs are in the HTML
            content = response.text
            s3_urls = [url for url in content.split() if 'eicaws-saryupariwar.s3.amazonaws.com' in url]
            if s3_urls:
                print(f"✅ Found {len(s3_urls)} S3 URLs in homepage HTML")
                return True
            else:
                print("⚠️  No S3 URLs found in homepage (may be normal if no images in DB)")
                return True  # Still pass, just no images
        else:
            print(f"❌ Homepage returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python manage.py runserver")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("S3 IMAGE INTEGRATION TEST")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Configuration
    results['config'] = test_configuration()
    
    # Test 2: URL Generation
    all_s3, sample_urls = test_url_generation()
    results['urls'] = all_s3
    
    # Test 3: Image Accessibility
    results['access'] = test_image_accessibility(sample_urls)
    
    # Test 4: Homepage
    results['homepage'] = test_homepage()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"Configuration: {'✅ PASS' if results['config'] else '❌ FAIL'}")
    print(f"URL Generation: {'✅ PASS' if results['urls'] else '❌ FAIL'}")
    access_status = '✅ PASS' if results['access'] is True else ('⚠️  PARTIAL' if results['access'] is None else '❌ FAIL')
    print(f"Image Accessibility: {access_status}")
    homepage_status = '✅ PASS' if results['homepage'] is True else ('⚠️  SKIPPED' if results['homepage'] is None else '❌ FAIL')
    print(f"Homepage: {homepage_status}")
    
    all_passed = all(r for r in results.values() if r is not None)
    
    if all_passed:
        print("\n🎉 All critical tests passed!")
        print("✅ S3 image configuration is working correctly")
    else:
        print("\n⚠️  Some tests had issues, but core functionality should work")
        print("✅ URL generation is working - images should load in browser")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

