#!/usr/bin/env python
"""
Script to populate database with content from the working website
Based on: http://44.201.152.56:8000/?next=/dashboard/
"""
import os
import sys
import django
from datetime import datetime, date

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from administration.models import SamajGallery, SamajEvent, Promotion, Testimonial
from django.core.files import File
from django.utils import timezone

def create_gallery_images():
    """Create gallery images for carousel"""
    print("Creating gallery images...")
    
    # Gallery images from working website
    gallery_data = [
        {'title': 'Samaj Image', 'image_path': 'media/samaj_gallery/samaj_image_1.jpg'},
        {'title': 'Samaj Image', 'image_path': 'media/samaj_gallery/samaj_image_2.jpg'},
        {'title': 'Image 9', 'image_path': 'media/samaj_gallery/image_9.jpg'},
        {'title': 'Image 10', 'image_path': 'media/samaj_gallery/image_10.jpg'},
        {'title': 'Image 11', 'image_path': 'media/samaj_gallery/image_11.jpg'},
        {'title': 'Image 12', 'image_path': 'media/samaj_gallery/image_12.jpg'},
    ]
    
    created = 0
    for item in gallery_data:
        # Check if already exists
        if not SamajGallery.objects.filter(title=item['title']).exists():
            gallery = SamajGallery.objects.create(
                title=item['title'],
                # Note: Image will be set via S3 URL or admin panel
            )
            # Set image name for S3 reference
            gallery.image.name = item['image_path']
            gallery.save()
            created += 1
            print(f"  ✓ Created: {item['title']}")
        else:
            print(f"  - Already exists: {item['title']}")
    
    print(f"Created {created} gallery images\n")
    return created

def create_events():
    """Create events from working website"""
    print("Creating events...")
    
    events_data = [
        {
            'title': 'Holi Sammelan',
            'date_of_event': date(2025, 3, 20),
        },
        {
            'title': 'Quarterly Meet',
            'date_of_event': date(2025, 3, 19),
        },
        {
            'title': 'Samaj Elections',
            'date_of_event': date(2025, 1, 24),
        },
        {
            'title': 'Parichay Sammelan',
            'date_of_event': date(2025, 1, 12),
        },
    ]
    
    created = 0
    for event_data in events_data:
        # Check if already exists
        if not SamajEvent.objects.filter(title=event_data['title'], date_of_event=event_data['date_of_event']).exists():
            SamajEvent.objects.create(**event_data)
            created += 1
            print(f"  ✓ Created: {event_data['title']} - {event_data['date_of_event']}")
        else:
            print(f"  - Already exists: {event_data['title']}")
    
    print(f"Created {created} events\n")
    return created

def create_testimonials():
    """Create testimonials from working website"""
    print("Creating testimonials...")
    
    testimonials_data = [
        {
            'testimony': 'A very nice platform to find ideal match for your children.The functionality is quite easy to learn even for not so technology familiar people.You can use it even on your phone with ease to search profiles.',
            'made_by': 'Surendra Dubey',
            'image_path': 'media/testimonials/surendra_dubey.jpg',
        },
        {
            'testimony': 'Excellent organisation of different events by the Saryuparin Brahmin samaj which keeps the entire community connected and united!!',
            'made_by': 'Aditya Tiwari',
            'image_path': 'media/testimonials/aditya_tiwari.jpg',
        },
        {
            'testimony': 'Saryparin brahmin samaj patrika has helped me to find a perfect match for my son !! Really appreciate the amazing work by the members of the society!!',
            'made_by': 'Dheeraj Shukla',
            'image_path': 'media/testimonials/dheeraj_shukla.jpg',
        },
    ]
    
    created = 0
    for testimonial_data in testimonials_data:
        # Check if already exists
        if not Testimonial.objects.filter(made_by=testimonial_data['made_by']).exists():
            testimonial = Testimonial.objects.create(
                testimony=testimonial_data['testimony'],
                made_by=testimonial_data['made_by'],
            )
            # Set image name for S3 reference
            testimonial.image.name = testimonial_data['image_path']
            testimonial.save()
            created += 1
            print(f"  ✓ Created: {testimonial_data['made_by']}")
        else:
            print(f"  - Already exists: {testimonial_data['made_by']}")
    
    print(f"Created {created} testimonials\n")
    return created

def create_promotions():
    """Create sample promotions"""
    print("Creating promotions...")
    
    # Promotions can be added via admin panel
    # For now, we'll create placeholder entries
    promotions_data = [
        {
            'advertiser_name': 'Community Event',
            'banner_path': 'media/promotions/promotion_1.jpg',
        },
        {
            'advertiser_name': 'Samaj Newsletter',
            'banner_path': 'media/promotions/promotion_2.jpg',
        },
    ]
    
    created = 0
    for promo_data in promotions_data:
        if not Promotion.objects.filter(advertiser_name=promo_data['advertiser_name']).exists():
            promotion = Promotion.objects.create(
                advertiser_name=promo_data['advertiser_name'],
            )
            promotion.banner.name = promo_data['banner_path']
            promotion.save()
            created += 1
            print(f"  ✓ Created: {promo_data['advertiser_name']}")
        else:
            print(f"  - Already exists: {promo_data['advertiser_name']}")
    
    print(f"Created {created} promotions\n")
    return created

def main():
    """Run all population functions"""
    print("=" * 60)
    print("POPULATING DATABASE WITH CONTENT")
    print("=" * 60)
    print()
    
    total_created = 0
    total_created += create_gallery_images()
    total_created += create_events()
    total_created += create_testimonials()
    total_created += create_promotions()
    
    print("=" * 60)
    print(f"SUMMARY: Created {total_created} items")
    print("=" * 60)
    print()
    print("Note: Images need to be uploaded to S3 bucket:")
    print("  - media/samaj_gallery/")
    print("  - media/testimonials/")
    print("  - media/promotions/")
    print()
    print("Or add images via Django admin panel.")

if __name__ == '__main__':
    main()

