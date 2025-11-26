#!/usr/bin/env python
"""
Fix existing database entries to have correct S3 paths
Remove 'media/' prefix since storage backend adds it
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import SamajGallery, Promotion, Testimonial

def fix_paths():
    """Fix image paths in database"""
    print("Fixing S3 image paths...")
    print("=" * 60)
    
    # Fix Gallery images
    print("\n📸 Fixing Gallery Images...")
    gallery_count = 0
    for gallery in SamajGallery.objects.all():
        if gallery.image.name and gallery.image.name.startswith('media/'):
            old_path = gallery.image.name
            new_path = gallery.image.name.replace('media/', '', 1)
            gallery.image.name = new_path
            gallery.save()
            print(f"  ✓ Fixed: {old_path} -> {new_path}")
            gallery_count += 1
    
    # Fix Promotion images
    print("\n📢 Fixing Promotion Images...")
    promo_count = 0
    for promo in Promotion.objects.all():
        if promo.banner.name and promo.banner.name.startswith('media/'):
            old_path = promo.banner.name
            new_path = promo.banner.name.replace('media/', '', 1)
            promo.banner.name = new_path
            promo.save()
            print(f"  ✓ Fixed: {old_path} -> {new_path}")
            promo_count += 1
    
    # Fix Testimonial images
    print("\n💬 Fixing Testimonial Images...")
    testimonial_count = 0
    for testimonial in Testimonial.objects.all():
        if testimonial.image.name and testimonial.image.name.startswith('media/'):
            old_path = testimonial.image.name
            new_path = testimonial.image.name.replace('media/', '', 1)
            testimonial.image.name = new_path
            testimonial.save()
            print(f"  ✓ Fixed: {old_path} -> {new_path}")
            testimonial_count += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Fixed Gallery: {gallery_count}")
    print(f"✅ Fixed Promotions: {promo_count}")
    print(f"✅ Fixed Testimonials: {testimonial_count}")
    print(f"✅ Total Fixed: {gallery_count + promo_count + testimonial_count}")

if __name__ == '__main__':
    fix_paths()

