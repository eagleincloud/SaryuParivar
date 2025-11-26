#!/usr/bin/env python
"""
Fetch all images from S3 and point website to them
Uses Django storage backend to access S3
Location: s3://eicaws-saryupariwar/media/
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from Saryupari_Brahmin_Project.settings import AWS_STORAGE_BUCKET_NAME
from administration.models import SamajGallery, Promotion, Testimonial
from Saryupari_Brahmin_Project.storages import MediaStorage
from django.core.files.storage import default_storage

def list_s3_images_using_storage():
    """List images using Django storage backend"""
    print(f"Fetching images from S3 bucket: {AWS_STORAGE_BUCKET_NAME}")
    print("=" * 60)
    
    storage = MediaStorage()
    images = {
        'gallery': [],
        'testimonials': [],
        'promotions': [],
        'other': []
    }
    
    try:
        # List all files in media/ directory
        # Note: This requires proper S3 access
        files = storage.listdir('media/')
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
        
        for file in files[1]:  # files[1] contains file names
            if not file.lower().endswith(image_extensions):
                continue
            
            full_path = f"media/{file}"
            
            # Categorize by folder or filename
            if 'samaj_gallery' in full_path.lower() or 'gallery' in full_path.lower():
                images['gallery'].append(full_path)
            elif 'testimonial' in full_path.lower():
                images['testimonials'].append(full_path)
            elif 'promotion' in full_path.lower() or 'banner' in full_path.lower():
                images['promotions'].append(full_path)
            else:
                images['other'].append(full_path)
        
        return images
    
    except Exception as e:
        print(f"Error listing files: {e}")
        print("\nTrying alternative method...")
        return list_s3_images_manual()

def list_s3_images_manual():
    """Manual method - you can add image paths here"""
    print("\n📝 Manual Image Path Method")
    print("=" * 60)
    print("Since S3 access requires valid credentials, you can:")
    print("1. Use AWS CLI: aws s3 ls s3://eicaws-saryupariwar/media/ --recursive")
    print("2. Or provide image paths manually")
    print()
    
    # Common image paths structure - you can modify these
    common_paths = {
        'gallery': [
            'media/samaj_gallery/samaj_image_1.jpg',
            'media/samaj_gallery/samaj_image_2.jpg',
            'media/samaj_gallery/image_9.jpg',
            'media/samaj_gallery/image_10.jpg',
            'media/samaj_gallery/image_11.jpg',
            'media/samaj_gallery/image_12.jpg',
        ],
        'testimonials': [
            'media/testimonials/surendra_dubey.jpg',
            'media/testimonials/aditya_tiwari.jpg',
            'media/testimonials/dheeraj_shukla.jpg',
        ],
        'promotions': [
            'media/promotions/promotion_1.jpg',
            'media/promotions/promotion_2.jpg',
        ]
    }
    
    return common_paths

def create_gallery_entries(image_keys):
    """Create SamajGallery entries pointing to S3 images"""
    print("\n📸 Creating Gallery Entries...")
    created = 0
    updated = 0
    
    for key in image_keys:
        # Extract title from filename
        filename = key.split('/')[-1]
        title = filename.replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('.gif', '').title()
        
        # Clean up title
        title = ' '.join(title.split())
        if not title:
            title = "Gallery Image"
        
        # Check if already exists (by image path)
        existing = SamajGallery.objects.filter(image=key).first()
        
        # Remove 'media/' prefix if present (storage backend adds it)
        s3_path = key.replace('media/', '', 1) if key.startswith('media/') else key
        
        if existing:
            print(f"  ✓ Already exists: {title} ({s3_path})")
            updated += 1
        else:
            gallery = SamajGallery.objects.create(title=title)
            # Point to S3 image (storage backend adds 'media/' prefix)
            gallery.image.name = s3_path
            gallery.save()
            created += 1
            print(f"  ✓ Created: {title}")
            print(f"    S3 Path: {s3_path}")
            print(f"    Full URL: {gallery.image.url}")
    
    print(f"\n  Summary: Created {created}, Updated {updated}")
    return created, updated

def create_promotion_entries(image_keys):
    """Create Promotion entries pointing to S3 images"""
    print("\n📢 Creating Promotion Entries...")
    created = 0
    updated = 0
    
    for key in image_keys:
        # Extract advertiser name from filename
        filename = key.split('/')[-1]
        advertiser_name = filename.replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('.gif', '').title()
        
        # Clean up name
        advertiser_name = ' '.join(advertiser_name.split())
        if not advertiser_name:
            advertiser_name = "Community Promotion"
        
        # Check if already exists
        existing = Promotion.objects.filter(banner=key).first()
        
        # Remove 'media/' prefix if present
        s3_path = key.replace('media/', '', 1) if key.startswith('media/') else key
        
        if existing:
            print(f"  ✓ Already exists: {advertiser_name} ({s3_path})")
            updated += 1
        else:
            promotion = Promotion.objects.create(advertiser_name=advertiser_name)
            promotion.banner.name = s3_path
            promotion.save()
            created += 1
            print(f"  ✓ Created: {advertiser_name}")
            print(f"    S3 Path: {s3_path}")
            print(f"    Full URL: {promotion.banner.url}")
    
    print(f"\n  Summary: Created {created}, Updated {updated}")
    return created, updated

def create_testimonial_entries(image_keys):
    """Create Testimonial entries pointing to S3 images"""
    print("\n💬 Creating Testimonial Entries...")
    created = 0
    updated = 0
    
    # Map known testimonial images to names
    testimonial_map = {
        'surendra': ('Surendra Dubey', 'A very nice platform to find ideal match for your children.The functionality is quite easy to learn even for not so technology familiar people.You can use it even on your phone with ease to search profiles.'),
        'aditya': ('Aditya Tiwari', 'Excellent organisation of different events by the Saryuparin Brahmin samaj which keeps the entire community connected and united!!'),
        'dheeraj': ('Dheeraj Shukla', 'Saryparin brahmin samaj patrika has helped me to find a perfect match for my son !! Really appreciate the amazing work by the members of the society!!'),
    }
    
    for key in image_keys:
        filename = key.lower()
        
        # Try to match with known names
        made_by = None
        testimony = None
        for key_name, (person_name, person_testimony) in testimonial_map.items():
            if key_name in filename:
                made_by = person_name
                testimony = person_testimony
                break
        
        if not made_by:
            # Extract from filename
            made_by = key.split('/')[-1].replace('_', ' ').replace('-', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').title()
            testimony = "Testimonial from our community member."
        
        # Check if already exists
        existing = Testimonial.objects.filter(made_by=made_by).first()
        
        # Remove 'media/' prefix if present
        s3_path = key.replace('media/', '', 1) if key.startswith('media/') else key
        
        if existing:
            # Update image if different
            if existing.image.name != s3_path:
                existing.image.name = s3_path
                existing.save()
                print(f"  ✓ Updated: {made_by} -> {s3_path}")
                updated += 1
            else:
                print(f"  ✓ Already exists: {made_by}")
        else:
            testimonial = Testimonial.objects.create(
                made_by=made_by,
                testimony=testimony
            )
            testimonial.image.name = s3_path
            testimonial.save()
            created += 1
            print(f"  ✓ Created: {made_by}")
            print(f"    S3 Path: {s3_path}")
            print(f"    Full URL: {testimonial.image.url}")
    
    print(f"\n  Summary: Created {created}, Updated {updated}")
    return created, updated

def main():
    """Main function"""
    print("=" * 60)
    print("FETCHING IMAGES FROM S3 AND POINTING WEBSITE TO THEM")
    print("=" * 60)
    print(f"Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"Location: s3://{AWS_STORAGE_BUCKET_NAME}/media/")
    print()
    
    # Try to list images
    images = list_s3_images_using_storage()
    
    # If no images found, use manual method
    total_images = sum(len(v) for v in images.values())
    if total_images == 0:
        print("\n⚠️  No images found via storage backend.")
        print("Using manual/common paths method...")
        images = list_s3_images_manual()
    
    # Print summary
    print("\n📊 Image Summary:")
    print(f"  Gallery Images: {len(images.get('gallery', []))}")
    print(f"  Testimonials: {len(images.get('testimonials', []))}")
    print(f"  Promotions: {len(images.get('promotions', []))}")
    print(f"  Other Images: {len(images.get('other', []))}")
    print(f"  Total: {sum(len(v) for v in images.values())}")
    
    # Show images
    if images.get('gallery'):
        print("\n📸 Gallery Images:")
        for img in images['gallery']:
            print(f"  - {img}")
    
    if images.get('testimonials'):
        print("\n💬 Testimonial Images:")
        for img in images['testimonials']:
            print(f"  - {img}")
    
    if images.get('promotions'):
        print("\n📢 Promotion Images:")
        for img in images['promotions']:
            print(f"  - {img}")
    
    # Create database entries
    print("\n" + "=" * 60)
    print("CREATING DATABASE ENTRIES")
    print("=" * 60)
    
    total_created = 0
    total_updated = 0
    
    # Create gallery entries
    if images.get('gallery'):
        created, updated = create_gallery_entries(images['gallery'])
        total_created += created
        total_updated += updated
    
    # Create promotion entries
    if images.get('promotions'):
        created, updated = create_promotion_entries(images['promotions'])
        total_created += created
        total_updated += updated
    
    # Create testimonial entries
    if images.get('testimonials'):
        created, updated = create_testimonial_entries(images['testimonials'])
        total_created += created
        total_updated += updated
    
    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Total Created: {total_created}")
    print(f"✅ Total Updated: {total_updated}")
    print(f"\n🌐 All images are now pointing to S3 bucket")
    print(f"   S3 URL: https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")
    print(f"\n✅ Website will display images directly from S3!")
    print("\n💡 Note: If images don't appear, verify:")
    print("   1. Images exist in S3 at the specified paths")
    print("   2. S3 bucket has public read access")
    print("   3. Image paths in database match S3 paths")

if __name__ == '__main__':
    main()

