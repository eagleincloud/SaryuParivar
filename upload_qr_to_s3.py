"""
Script to upload QR code image to S3
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from django.conf import settings
from Saryupari_Brahmin_Project.s3_utils import upload_to_s3, get_s3_client, check_s3_object_exists
import mimetypes

def upload_qr_code():
    """Upload QR code image to S3"""
    # Path to QR code image
    qr_code_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'qr_code.jpeg')
    
    if not os.path.exists(qr_code_path):
        print(f"❌ QR code image not found at: {qr_code_path}")
        print("Please ensure the QR code image file exists at static/images/qr_code.jpeg")
        return False
    
    # Read the image file
    try:
        with open(qr_code_path, 'rb') as f:
            file_content = f.read()
        print(f"✅ Read QR code image: {len(file_content)} bytes")
    except Exception as e:
        print(f"❌ Error reading QR code image: {e}")
        return False
    
    # S3 bucket and key
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = 'media/qr_code.jpeg'  # Store in media/ folder
    
    # Check if file already exists
    if check_s3_object_exists(bucket_name, s3_key):
        print(f"⚠️  File already exists in S3: {s3_key}")
        response = input("Do you want to overwrite it? (yes/no): ")
        if response.lower() != 'yes':
            print("Upload cancelled.")
            return False
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(qr_code_path)
    if not content_type:
        content_type = 'image/jpeg'  # Default to JPEG
    
    print(f"📤 Uploading QR code to S3...")
    print(f"   Bucket: {bucket_name}")
    print(f"   Key: {s3_key}")
    print(f"   Content-Type: {content_type}")
    
    # Upload to S3
    success = upload_to_s3(file_content, bucket_name, s3_key, content_type)
    
    if success:
        print(f"✅ Successfully uploaded QR code to S3!")
        print(f"   URL: /media/qr_code.jpeg")
        print(f"   Full S3 path: s3://{bucket_name}/{s3_key}")
        return True
    else:
        print(f"❌ Failed to upload QR code to S3")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("QR Code Upload to S3")
    print("=" * 60)
    
    # Check S3 client
    s3_client = get_s3_client()
    if not s3_client:
        print("❌ Failed to create S3 client. Check AWS credentials in pod.env")
        sys.exit(1)
    
    print("✅ S3 client created successfully")
    print()
    
    # Upload QR code
    success = upload_qr_code()
    
    if success:
        print()
        print("=" * 60)
        print("✅ Upload Complete!")
        print("=" * 60)
        print("Next steps:")
        print("1. Update payment.html template to use: /media/qr_code.jpeg")
        print("2. The image will be served through Django view from S3")
    else:
        print()
        print("=" * 60)
        print("❌ Upload Failed")
        print("=" * 60)
        sys.exit(1)

