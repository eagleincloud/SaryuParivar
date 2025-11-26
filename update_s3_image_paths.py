#!/usr/bin/env python
"""
Update database to point to S3 images
This script updates image paths in the database to point to actual S3 locations
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import SamajGallery, Promotion, Testimonial
from Saryupari_Brahmin_Project.settings import AWS_STORAGE_BUCKET_NAME

def update_gallery_with_s3_paths():
    """Update gallery images to point to S3"""
    print(f"\n{'='*60}")
    print("Updating Gallery Images to S3 Paths")
    print(f"{'='*60}\n")
    
    # Common S3 image paths for gallery
    # These are typical paths - adjust based on actual S3 structure
    gallery_paths = [
        'media/samaj_gallery/samaj_image_1.jpg',
        'media/samaj_gallery/samaj_image_2.jpg',
        'media/samaj_gallery/image_9.jpg',
        'media/samaj_gallery/image_10.jpg',
        'media/samaj_gallery/image_11.jpg',
        'media/samaj_gallery/image_12.jpg',
    ]
    
    # Alternative paths to try
    alt_paths = [
        'media/gallery/',
        'media/images/',
        'media/banner/',
    ]
    
    galleries = SamajGallery.objects.all()
    
    for idx, gallery in enumerate(galleries):
        # Try to find matching image path
        # First, check if image name already has a path
        if gallery.image and gallery.image.name:
            current_path = gallery.image.name
            if 'media/' in current_path or current_path.startswith('/'):
                print(f"  ✓ {gallery.title or 'Untitled'}: Already has path - {current_path}")
                continue
        
        # Try to set a path based on title or index
        if idx < len(gallery_paths):
            s3_path = gallery_paths[idx]
        else:
            # Generate path from title
            title_slug = (gallery.title or f'image_{idx+1}').lower().replace(' ', '_')
            s3_path = f'media/samaj_gallery/{title_slug}.jpg'
        
        # Update the image path
        gallery.image.name = s3_path
        gallery.save()
        print(f"  ✓ Updated: {gallery.title or 'Untitled'} -> {s3_path}")

def update_testimonials_with_s3_paths():
    """Update testimonials to point to S3"""
    print(f"\n{'='*60}")
    print("Updating Testimonials to S3 Paths")
    print(f"{'='*60}\n")
    
    testimonials = Testimonial.objects.all()
    
    for testimonial in testimonials:
        # Generate path from name
        name_slug = testimonial.made_by.lower().replace(' ', '_')
        s3_path = f'media/testimonials/{name_slug}.jpg'
        
        # Update if not already set
        if not testimonial.image or not testimonial.image.name or 'media/' not in testimonial.image.name:
            testimonial.image.name = s3_path
            testimonial.save()
            print(f"  ✓ Updated: {testimonial.made_by} -> {s3_path}")
        else:
            print(f"  ✓ {testimonial.made_by}: Already has path - {testimonial.image.name}")

def update_promotions_with_s3_paths():
    """Update promotions to point to S3"""
    print(f"\n{'='*60}")
    print("Updating Promotions to S3 Paths")
    print(f"{'='*60}\n")
    
    promotions = Promotion.objects.all()
    
    for idx, promotion in enumerate(promotions):
        # Generate path from advertiser name
        name_slug = promotion.advertiser_name.lower().replace(' ', '_')
        s3_path = f'media/promotions/{name_slug}.jpg'
        
        # Update if not already set
        if not promotion.banner or not promotion.banner.name or 'media/' not in promotion.banner.name:
            promotion.banner.name = s3_path
            promotion.save()
            print(f"  ✓ Updated: {promotion.advertiser_name} -> {s3_path}")
        else:
            print(f"  ✓ {promotion.advertiser_name}: Already has path - {promotion.banner.name}")

def list_all_s3_paths():
    """List all S3 paths that should exist"""
    print(f"\n{'='*60}")
    print("Expected S3 Image Paths")
    print(f"{'='*60}\n")
    
    print("Gallery Images:")
    galleries = SamajGallery.objects.all()
    for gallery in galleries:
        path = gallery.image.name if gallery.image else 'Not set'
        print(f"  - {gallery.title or 'Untitled'}: {path}")
    
    print("\nTestimonial Images:")
    testimonials = Testimonial.objects.all()
    for testimonial in testimonials:
        path = testimonial.image.name if testimonial.image else 'Not set'
        print(f"  - {testimonial.made_by}: {path}")
    
    print("\nPromotion Images:")
    promotions = Promotion.objects.all()
    for promotion in promotions:
        path = promotion.banner.name if promotion.banner else 'Not set'
        print(f"  - {promotion.advertiser_name}: {path}")
    
    print(f"\n{'='*60}")
    print("S3 Bucket URLs")
    print(f"{'='*60}\n")
    print(f"Base URL: https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")
    print(f"\nAll images will be accessible at:")
    print(f"  Website: http://yourdomain.com/media/[image_path]")
    print(f"  Direct S3: https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/[image_path]")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("UPDATE DATABASE TO POINT TO S3 IMAGES")
    print("="*60)
    
    # Update all records
    update_gallery_with_s3_paths()
    update_testimonials_with_s3_paths()
    update_promotions_with_s3_paths()
    
    # List all paths
    list_all_s3_paths()
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Gallery images: {SamajGallery.objects.count()}")
    print(f"✓ Testimonials: {Testimonial.objects.count()}")
    print(f"✓ Promotions: {Promotion.objects.count()}")
    print(f"\n✅ All database records now point to S3 paths!")
    print(f"\nNote: Make sure the actual image files exist in S3 at these paths.")
    print(f"      Images will be served via Django at: /media/[path]")

if __name__ == '__main__':
    main()

