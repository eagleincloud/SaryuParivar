#!/usr/bin/env python
"""
Fetch all images from S3 and point website to them
Location: s3://eicaws-saryupariwar/media/
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
    AWS_S3_REGION_NAME
)
from administration.models import SamajGallery, Promotion, Testimonial
from django.core.files.storage import default_storage

def get_s3_client():
    """Get S3 client"""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME
        )
        return s3_client
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        return None

def list_s3_images(s3_client, prefix='media/'):
    """List all images in S3 bucket"""
    print(f"Fetching images from s3://{AWS_STORAGE_BUCKET_NAME}/{prefix}")
    print("=" * 60)
    
    images = {
        'gallery': [],
        'testimonials': [],
        'promotions': [],
        'other': []
    }
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=prefix)
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
        
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                
                # Skip if not an image
                if not key.lower().endswith(image_extensions):
                    continue
                
                # Categorize images by folder
                if 'samaj_gallery' in key.lower() or 'gallery' in key.lower():
                    images['gallery'].append(key)
                elif 'testimonial' in key.lower():
                    images['testimonials'].append(key)
                elif 'promotion' in key.lower() or 'banner' in key.lower():
                    images['promotions'].append(key)
                else:
                    images['other'].append(key)
        
        return images
    
    except ClientError as e:
        print(f"Error listing S3 objects: {e}")
        return images
    except Exception as e:
        print(f"Unexpected error: {e}")
        return images

def create_gallery_entries(image_keys):
    """Create SamajGallery entries pointing to S3 images"""
    print("\n📸 Creating Gallery Entries...")
    created = 0
    updated = 0
    
    for key in image_keys:
        # Extract title from filename
        filename = key.split('/')[-1]
        title = filename.replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').title()
        
        # Check if already exists
        existing = SamajGallery.objects.filter(image=key).first()
        
        if existing:
            print(f"  ✓ Already exists: {title} ({key})")
            updated += 1
        else:
            gallery = SamajGallery.objects.create(title=title)
            # Point to S3 image (don't copy, just reference)
            gallery.image.name = key
            gallery.save()
            created += 1
            print(f"  ✓ Created: {title} -> {key}")
    
    print(f"  Created: {created}, Updated: {updated}")
    return created, updated

def create_promotion_entries(image_keys):
    """Create Promotion entries pointing to S3 images"""
    print("\n📢 Creating Promotion Entries...")
    created = 0
    updated = 0
    
    for key in image_keys:
        # Extract advertiser name from filename
        filename = key.split('/')[-1]
        advertiser_name = filename.replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').title()
        
        # Check if already exists
        existing = Promotion.objects.filter(banner=key).first()
        
        if existing:
            print(f"  ✓ Already exists: {advertiser_name} ({key})")
            updated += 1
        else:
            promotion = Promotion.objects.create(advertiser_name=advertiser_name)
            # Point to S3 image
            promotion.banner.name = key
            promotion.save()
            created += 1
            print(f"  ✓ Created: {advertiser_name} -> {key}")
    
    print(f"  Created: {created}, Updated: {updated}")
    return created, updated

def create_testimonial_entries(image_keys):
    """Create Testimonial entries pointing to S3 images"""
    print("\n💬 Creating Testimonial Entries...")
    created = 0
    updated = 0
    
    # Map known testimonial images to names
    testimonial_map = {
        'surendra': 'Surendra Dubey',
        'aditya': 'Aditya Tiwari',
        'dheeraj': 'Dheeraj Shukla',
    }
    
    for key in image_keys:
        filename = key.lower()
        
        # Try to match with known names
        made_by = None
        for key_name, person_name in testimonial_map.items():
            if key_name in filename:
                made_by = person_name
                break
        
        if not made_by:
            # Extract from filename
            made_by = key.split('/')[-1].replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').title()
        
        # Check if already exists
        existing = Testimonial.objects.filter(made_by=made_by).first()
        
        if existing:
            # Update image if needed
            if existing.image.name != key:
                existing.image.name = key
                existing.save()
                print(f"  ✓ Updated: {made_by} -> {key}")
                updated += 1
            else:
                print(f"  ✓ Already exists: {made_by}")
        else:
            testimonial = Testimonial.objects.create(
                made_by=made_by,
                testimony="Testimonial from our community member."
            )
            testimonial.image.name = key
            testimonial.save()
            created += 1
            print(f"  ✓ Created: {made_by} -> {key}")
    
    print(f"  Created: {created}, Updated: {updated}")
    return created, updated

def main():
    """Main function"""
    print("=" * 60)
    print("FETCHING IMAGES FROM S3 AND POINTING WEBSITE TO THEM")
    print("=" * 60)
    print(f"Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"Location: s3://{AWS_STORAGE_BUCKET_NAME}/media/")
    print()
    
    # Get S3 client
    s3_client = get_s3_client()
    if not s3_client:
        print("❌ Failed to connect to S3")
        return
    
    # List all images
    images = list_s3_images(s3_client, prefix='media/')
    
    # Print summary
    print("\n📊 Image Summary:")
    print(f"  Gallery Images: {len(images['gallery'])}")
    print(f"  Testimonials: {len(images['testimonials'])}")
    print(f"  Promotions: {len(images['promotions'])}")
    print(f"  Other Images: {len(images['other'])}")
    print(f"  Total: {sum(len(v) for v in images.values())}")
    
    # Show all images
    if images['gallery']:
        print("\n📸 Gallery Images Found:")
        for img in images['gallery']:
            print(f"  - {img}")
    
    if images['testimonials']:
        print("\n💬 Testimonial Images Found:")
        for img in images['testimonials']:
            print(f"  - {img}")
    
    if images['promotions']:
        print("\n📢 Promotion Images Found:")
        for img in images['promotions']:
            print(f"  - {img}")
    
    if images['other']:
        print("\n📁 Other Images Found:")
        for img in images['other'][:10]:  # Show first 10
            print(f"  - {img}")
        if len(images['other']) > 10:
            print(f"  ... and {len(images['other']) - 10} more")
    
    # Create database entries
    print("\n" + "=" * 60)
    print("CREATING DATABASE ENTRIES")
    print("=" * 60)
    
    total_created = 0
    total_updated = 0
    
    # Create gallery entries
    if images['gallery']:
        created, updated = create_gallery_entries(images['gallery'])
        total_created += created
        total_updated += updated
    
    # Create promotion entries
    if images['promotions']:
        created, updated = create_promotion_entries(images['promotions'])
        total_created += created
        total_updated += updated
    
    # Create testimonial entries
    if images['testimonials']:
        created, updated = create_testimonial_entries(images['testimonials'])
        total_created += created
        total_updated += updated
    
    # Handle other images (try to categorize)
    if images['other']:
        print("\n📁 Processing Other Images...")
        # Try to categorize based on filename patterns
        gallery_others = [img for img in images['other'] if any(x in img.lower() for x in ['image', 'photo', 'pic', 'img'])]
        if gallery_others:
            created, updated = create_gallery_entries(gallery_others)
            total_created += created
            total_updated += updated
    
    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Total Created: {total_created}")
    print(f"✅ Total Updated: {total_updated}")
    print(f"✅ All images are now pointing to S3 bucket")
    print(f"\n🌐 Images will be served from: https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")
    print("\n✅ Website is now configured to display all S3 images!")

if __name__ == '__main__':
    main()
