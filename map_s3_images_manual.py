#!/usr/bin/env python
"""
Manually map S3 images to database records
This script updates database to point to S3 images based on common patterns
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import SamajGallery, Promotion, Testimonial

def map_gallery_images():
    """Map gallery images to S3 paths"""
    print("\n=== Mapping Gallery Images ===")
    
    # Common S3 paths for gallery images
    # These are typical paths - adjust based on your S3 structure
    gallery_paths = [
        'samaj_gallery/samaj_image_1.jpg',
        'samaj_gallery/samaj_image_2.jpg',
        'samaj_gallery/image_9.jpg',
        'samaj_gallery/image_10.jpg',
        'samaj_gallery/image_11.jpg',
        'samaj_gallery/image_12.jpg',
        'samaj_gallery/banner_1.jpg',
        'samaj_gallery/banner_2.jpg',
    ]
    
    galleries = list(SamajGallery.objects.all())
    
    for idx, gallery in enumerate(galleries):
        if idx < len(gallery_paths):
            gallery.image.name = gallery_paths[idx]
            gallery.save()
            print(f"✓ Mapped: {gallery.title} -> {gallery_paths[idx]}")
        else:
            # Try to find image by title
            title_lower = gallery.title.lower().replace(' ', '_')
            possible_paths = [
                f'samaj_gallery/{title_lower}.jpg',
                f'samaj_gallery/{title_lower}.jpeg',
                f'samaj_gallery/{title_lower}.png',
                f'media/samaj_gallery/{title_lower}.jpg',
            ]
            # Just set a default path - actual image should be in S3
            if not gallery.image.name:
                gallery.image.name = f'samaj_gallery/{title_lower}.jpg'
                gallery.save()
                print(f"✓ Set default path: {gallery.title} -> {gallery.image.name}")

def map_testimonials():
    """Map testimonial images to S3 paths"""
    print("\n=== Mapping Testimonials ===")
    
    # Map based on testimonial author names
    testimonial_mapping = {
        'Surendra Dubey': 'testimonials/surendra_dubey.jpg',
        'Aditya Tiwari': 'testimonials/aditya_tiwari.jpg',
        'Dheeraj Shukla': 'testimonials/dheeraj_shukla.jpg',
    }
    
    testimonials = Testimonial.objects.all()
    
    for testimonial in testimonials:
        if testimonial.made_by in testimonial_mapping:
            testimonial.image.name = testimonial_mapping[testimonial.made_by]
            testimonial.save()
            print(f"✓ Mapped: {testimonial.made_by} -> {testimonial_mapping[testimonial.made_by]}")
        else:
            # Create path from name
            name_lower = testimonial.made_by.lower().replace(' ', '_')
            testimonial.image.name = f'testimonials/{name_lower}.jpg'
            testimonial.save()
            print(f"✓ Set path: {testimonial.made_by} -> {testimonial.image.name}")

def map_promotions():
    """Map promotion images to S3 paths"""
    print("\n=== Mapping Promotions ===")
    
    promotions = Promotion.objects.all()
    
    for idx, promotion in enumerate(promotions):
        name_lower = promotion.advertiser_name.lower().replace(' ', '_')
        promotion.banner.name = f'promotions/{name_lower}.jpg'
        promotion.save()
        print(f"✓ Mapped: {promotion.advertiser_name} -> {promotion.banner.name}")

def main():
    """Main function"""
    print("=" * 60)
    print("MAPPING S3 IMAGE PATHS TO DATABASE")
    print("=" * 60)
    print("\nThis script sets image paths in database to point to S3.")
    print("Images will be served via Django views using boto3.")
    print("\nNote: Make sure images exist in S3 at these paths!")
    
    map_gallery_images()
    map_testimonials()
    map_promotions()
    
    print("\n" + "=" * 60)
    print("✅ MAPPING COMPLETE")
    print("=" * 60)
    print("\nAll database records now point to S3 image paths.")
    print("Images will be loaded from: https://eicaws-saryupariwar.s3.amazonaws.com/media/")
    print("\nTo verify images exist in S3, update AWS credentials and run:")
    print("  python manage.py sync_s3_images --dry-run")

if __name__ == '__main__':
    main()

