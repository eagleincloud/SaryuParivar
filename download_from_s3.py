"""
Script to download logo and QR code from S3 to EC2
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from django.conf import settings
from Saryupari_Brahmin_Project.s3_utils import get_s3_object, get_s3_client
import mimetypes

def download_from_s3(s3_key, local_path):
    """Download a file from S3 to local filesystem"""
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    print(f"📥 Downloading from S3: s3://{bucket_name}/{s3_key}")
    print(f"   To local: {local_path}")
    
    # Get file from S3
    content, content_type = get_s3_object(bucket_name, s3_key)
    
    if content is None:
        print(f"❌ File not found in S3: {s3_key}")
        return False
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Write to local file
    try:
        with open(local_path, 'wb') as f:
            f.write(content)
        print(f"✅ Successfully downloaded: {len(content)} bytes")
        print(f"   Content-Type: {content_type}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Download logo and QR code from S3"""
    print("=" * 60)
    print("Download Images from S3 to EC2")
    print("=" * 60)
    
    base_dir = settings.BASE_DIR
    static_images_dir = os.path.join(base_dir, 'static', 'images')
    
    # Download logo
    print("\n1. Downloading Logo...")
    logo_s3_key = 'media/saryu-parivaar-logo.png'
    logo_local_path = os.path.join(static_images_dir, 'saryu-parivaar-logo.png')
    logo_success = download_from_s3(logo_s3_key, logo_local_path)
    
    # Download QR code
    print("\n2. Downloading QR Code...")
    qr_s3_key = 'media/qr_code.jpeg'
    qr_local_path = os.path.join(static_images_dir, 'qr_code.jpeg')
    qr_success = download_from_s3(qr_s3_key, qr_local_path)
    
    print("\n" + "=" * 60)
    if logo_success and qr_success:
        print("✅ All files downloaded successfully!")
        print("=" * 60)
        print("\nDownloaded files:")
        print(f"  - Logo: {logo_local_path}")
        print(f"  - QR Code: {qr_local_path}")
        return True
    else:
        print("❌ Some files failed to download")
        print("=" * 60)
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

