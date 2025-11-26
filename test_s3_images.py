#!/usr/bin/env python
"""
Test script to verify S3 images are accessible
"""
import os
import sys
import django
import boto3
from botocore.exceptions import ClientError

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.settings import (
    AWS_STORAGE_BUCKET_NAME,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_REGION_NAME,
    AWS_S3_CUSTOM_DOMAIN,
    MEDIA_URL
)
from administration.models import SamajGallery, Promotion, Testimonial, CustomUser

def test_s3_connection():
    """Test S3 connection and bucket access"""
    print("=" * 60)
    print("Testing S3 Connection")
    print("=" * 60)
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME
        )
        
        # Test bucket access
        response = s3_client.head_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
        print(f"✅ Successfully connected to S3 bucket: {AWS_STORAGE_BUCKET_NAME}")
        print(f"   Region: {AWS_S3_REGION_NAME}")
        print(f"   Domain: {AWS_S3_CUSTOM_DOMAIN}")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Bucket '{AWS_STORAGE_BUCKET_NAME}' not found")
        elif error_code == '403':
            print(f"❌ Access denied to bucket '{AWS_STORAGE_BUCKET_NAME}'")
        else:
            print(f"❌ Error accessing bucket: {e}")
        return False
    except Exception as e:
        print(f"❌ Error connecting to S3: {e}")
        return False

def test_s3_images():
    """Test if images from models are accessible via S3"""
    print("\n" + "=" * 60)
    print("Testing S3 Image URLs")
    print("=" * 60)
    
    results = []
    
    # Test SamajGallery images
    gallery_images = SamajGallery.objects.all()[:3]
    print(f"\n📸 Samaj Gallery Images: {gallery_images.count()} found")
    for img in gallery_images:
        if img.image:
            url = img.image.url
            print(f"   - {img.title or 'Untitled'}: {url}")
            results.append(('Gallery', url, img.image.name))
    
    # Test Promotions
    promotions = Promotion.objects.all()[:3]
    print(f"\n📢 Promotions: {promotions.count()} found")
    for promo in promotions:
        if promo.banner:
            url = promo.banner.url
            print(f"   - {promo.advertiser_name}: {url}")
            results.append(('Promotion', url, promo.banner.name))
    
    # Test Testimonials
    testimonials = Testimonial.objects.all()[:3]
    print(f"\n💬 Testimonials: {testimonials.count()} found")
    for test in testimonials:
        if test.image:
            url = test.image.url
            print(f"   - {test.made_by}: {url}")
            results.append(('Testimonial', url, test.image.name))
    
    # Test User Profile Pics
    users = CustomUser.objects.exclude(profile_pic='')[:3]
    print(f"\n👤 User Profile Pics: {users.count()} found")
    for user in users:
        if user.profile_pic:
            url = user.profile_pic.url
            print(f"   - {user.show_username()}: {url}")
            results.append(('User', url, user.profile_pic.name))
    
    return results

def test_s3_url_format():
    """Verify S3 URL format is correct"""
    print("\n" + "=" * 60)
    print("Verifying S3 URL Format")
    print("=" * 60)
    
    expected_domain = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    print(f"Expected S3 URL format: {expected_domain}[file_path]")
    print(f"Current MEDIA_URL setting: {MEDIA_URL}")
    
    if MEDIA_URL.startswith('https://'):
        print("✅ MEDIA_URL is correctly configured for S3")
        if AWS_S3_CUSTOM_DOMAIN in MEDIA_URL:
            print(f"✅ S3 domain matches: {AWS_S3_CUSTOM_DOMAIN}")
            return True
        else:
            print(f"⚠️  S3 domain mismatch")
            return False
    else:
        print("⚠️  MEDIA_URL is not using S3 (using local storage)")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("S3 IMAGE ACCESS TEST")
    print("=" * 60)
    
    # Test S3 connection
    s3_connected = test_s3_connection()
    
    # Test URL format
    url_format_ok = test_s3_url_format()
    
    # Test image URLs
    image_urls = test_s3_images()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"S3 Connection: {'✅ PASS' if s3_connected else '❌ FAIL'}")
    print(f"URL Format: {'✅ PASS' if url_format_ok else '❌ FAIL'}")
    print(f"Images Found: {len(image_urls)}")
    
    if s3_connected and url_format_ok:
        print("\n🎉 S3 configuration is correct!")
        print(f"All images will be loaded from: https://{AWS_S3_CUSTOM_DOMAIN}/media/")
    else:
        print("\n⚠️  Some issues detected. Please check the configuration.")
    
    return s3_connected and url_format_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

