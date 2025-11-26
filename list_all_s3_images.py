#!/usr/bin/env python
"""
List ALL images from S3 bucket and create database entries
Run this after updating AWS credentials in pod.env
Location: s3://eicaws-saryupariwar/media/
"""
import os
import sys
import django
import boto3
from botocore.exceptions import ClientError

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.settings import (
    AWS_STORAGE_BUCKET_NAME,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_REGION_NAME
)
from administration.models import SamajGallery, Promotion, Testimonial

def list_all_s3_images():
    """List ALL images from S3 bucket"""
    print("=" * 60)
    print("LISTING ALL IMAGES FROM S3")
    print("=" * 60)
    print(f"Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"Prefix: media/")
    print()
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME
        )
        
        images = {
            'gallery': [],
            'testimonials': [],
            'promotions': [],
            'other': []
        }
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
        
        # List all objects with pagination
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix='media/')
        
        total_found = 0
        for page in pages:
            if 'Contents' not in page:
                continue
            
            for obj in page['Contents']:
                key = obj['Key']
                
                # Skip if not an image
                if not key.lower().endswith(image_extensions):
                    continue
                
                total_found += 1
                
                # Remove 'media/' prefix for database storage
                db_path = key.replace('media/', '', 1) if key.startswith('media/') else key
                
                # Categorize
                if 'samaj_gallery' in key.lower() or 'gallery' in key.lower():
                    images['gallery'].append(db_path)
                elif 'testimonial' in key.lower():
                    images['testimonials'].append(db_path)
                elif 'promotion' in key.lower() or 'banner' in key.lower():
                    images['promotions'].append(db_path)
                else:
                    images['other'].append(db_path)
        
        print(f"✅ Found {total_found} images in S3")
        print(f"\n📊 Breakdown:")
        print(f"  Gallery: {len(images['gallery'])}")
        print(f"  Testimonials: {len(images['testimonials'])}")
        print(f"  Promotions: {len(images['promotions'])}")
        print(f"  Other: {len(images['other'])}")
        
        return images
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidAccessKeyId':
            print("❌ Invalid AWS Access Key")
            print("   Please update AWS credentials in pod.env file")
        elif error_code == 'AccessDenied':
            print("❌ Access Denied to S3 bucket")
            print("   Please check IAM permissions")
        else:
            print(f"❌ Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def create_entries_from_s3(images):
    """Create database entries from S3 image list"""
    if not images:
        return
    
    print("\n" + "=" * 60)
    print("CREATING DATABASE ENTRIES")
    print("=" * 60)
    
    total_created = 0
    
    # Gallery
    if images['gallery']:
        print("\n📸 Creating Gallery Entries...")
        for path in images['gallery']:
            filename = path.split('/')[-1]
            title = filename.replace('_', ' ').replace('-', ' ').split('.')[0].title()
            
            if not SamajGallery.objects.filter(image=path).exists():
                gallery = SamajGallery.objects.create(title=title)
                gallery.image.name = path
                gallery.save()
                total_created += 1
                print(f"  ✓ {title}")
    
    # Promotions
    if images['promotions']:
        print("\n📢 Creating Promotion Entries...")
        for path in images['promotions']:
            filename = path.split('/')[-1]
            name = filename.replace('_', ' ').replace('-', ' ').split('.')[0].title()
            
            if not Promotion.objects.filter(banner=path).exists():
                promo = Promotion.objects.create(advertiser_name=name)
                promo.banner.name = path
                promo.save()
                total_created += 1
                print(f"  ✓ {name}")
    
    # Testimonials
    if images['testimonials']:
        print("\n💬 Creating Testimonial Entries...")
        for path in images['testimonials']:
            filename = path.split('/')[-1].lower()
            name = filename.replace('_', ' ').replace('-', ' ').split('.')[0].title()
            
            if not Testimonial.objects.filter(image=path).exists():
                testimonial = Testimonial.objects.create(
                    made_by=name,
                    testimony="Testimonial from our community member."
                )
                testimonial.image.name = path
                testimonial.save()
                total_created += 1
                print(f"  ✓ {name}")
    
    print(f"\n✅ Created {total_created} new entries")

def main():
    """Main function"""
    images = list_all_s3_images()
    
    if images:
        create_entries_from_s3(images)
        print("\n" + "=" * 60)
        print("✅ COMPLETE!")
        print("=" * 60)
        print("All images from S3 are now pointing to your website!")
        print(f"\n🌐 Images will be served from:")
        print(f"   https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/")
    else:
        print("\n⚠️  Could not access S3. Please:")
        print("   1. Update AWS credentials in pod.env")
        print("   2. Ensure bucket has proper permissions")
        print("   3. Run this script again")

if __name__ == '__main__':
    main()

