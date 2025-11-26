"""
Django management command to sync S3 images to database
Usage: python manage.py sync_s3_images
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from administration.models import SamajGallery, Promotion, Testimonial
import os
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class Command(BaseCommand):
    help = 'Sync images from S3 bucket to database records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('SYNCING S3 IMAGES TO DATABASE'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Get S3 client
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            self.stdout.write(self.style.SUCCESS(f'\n✓ Connected to S3: {settings.AWS_STORAGE_BUCKET_NAME}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error connecting to S3: {e}'))
            return
        
        # List all images
        all_images = self.list_all_images(s3_client)
        
        # Categorize images
        gallery_images = [img for img in all_images if 'gallery' in img.lower() or 'samaj' in img.lower()]
        testimonial_images = [img for img in all_images if 'testimonial' in img.lower()]
        promotion_images = [img for img in all_images if 'promotion' in img.lower() or 'banner' in img.lower()]
        
        self.stdout.write(f'\nFound images:')
        self.stdout.write(f'  Gallery: {len(gallery_images)}')
        self.stdout.write(f'  Testimonials: {len(testimonial_images)}')
        self.stdout.write(f'  Promotions: {len(promotion_images)}')
        
        # Update gallery
        self.sync_gallery(gallery_images, dry_run)
        
        # Update testimonials
        self.sync_testimonials(testimonial_images, dry_run)
        
        # Update promotions
        self.sync_promotions(promotion_images, dry_run)
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ SYNC COMPLETE'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def list_all_images(self, s3_client):
        """List all images in S3"""
        images = []
        try:
            paginator = s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Prefix='media/'
            )
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                            images.append(key)
            
            return images
        except ClientError as e:
            self.stdout.write(self.style.ERROR(f'Error listing S3: {e}'))
            return []

    def sync_gallery(self, s3_images, dry_run):
        """Sync gallery images"""
        self.stdout.write('\n=== Gallery Images ===')
        
        if not s3_images:
            self.stdout.write(self.style.WARNING('No gallery images found in S3'))
            return
        
        # Get existing galleries
        galleries = list(SamajGallery.objects.all())
        
        for idx, s3_path in enumerate(s3_images):
            # Remove 'media/' prefix for Django storage
            image_path = s3_path[6:] if s3_path.startswith('media/') else s3_path
            
            if idx < len(galleries):
                # Update existing
                gallery = galleries[idx]
                if not dry_run:
                    gallery.image.name = image_path
                    gallery.save()
                self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}✓ Updated: {gallery.title} -> {s3_path}")
            else:
                # Create new
                title = os.path.basename(image_path).replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('_', ' ').title()
                if not dry_run:
                    gallery = SamajGallery.objects.create(title=title)
                    gallery.image.name = image_path
                    gallery.save()
                self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}✓ Created: {title} -> {s3_path}")

    def sync_testimonials(self, s3_images, dry_run):
        """Sync testimonial images"""
        self.stdout.write('\n=== Testimonials ===')
        
        if not s3_images:
            self.stdout.write(self.style.WARNING('No testimonial images found in S3'))
            return
        
        testimonials = list(Testimonial.objects.all())
        
        for idx, s3_path in enumerate(s3_images):
            image_path = s3_path[6:] if s3_path.startswith('media/') else s3_path
            
            if idx < len(testimonials):
                testimonial = testimonials[idx]
                if not dry_run:
                    testimonial.image.name = image_path
                    testimonial.save()
                self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}✓ Updated: {testimonial.made_by} -> {s3_path}")

    def sync_promotions(self, s3_images, dry_run):
        """Sync promotion images"""
        self.stdout.write('\n=== Promotions ===')
        
        if not s3_images:
            self.stdout.write(self.style.WARNING('No promotion images found in S3'))
            return
        
        promotions = list(Promotion.objects.all())
        
        for idx, s3_path in enumerate(s3_images):
            image_path = s3_path[6:] if s3_path.startswith('media/') else s3_path
            
            if idx < len(promotions):
                promotion = promotions[idx]
                if not dry_run:
                    promotion.banner.name = image_path
                    promotion.save()
                self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}✓ Updated: {promotion.advertiser_name} -> {s3_path}")
            else:
                advertiser_name = os.path.basename(image_path).replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('_', ' ').title()
                if not dry_run:
                    promotion = Promotion.objects.create(advertiser_name=advertiser_name)
                    promotion.banner.name = image_path
                    promotion.save()
                self.stdout.write(f"{'[DRY RUN] ' if dry_run else ''}✓ Created: {advertiser_name} -> {s3_path}")

