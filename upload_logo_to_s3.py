"""
Script to upload logo image to S3
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

def upload_logo(logo_path=None):
    """Upload logo image to S3"""
    # Default logo path
    if not logo_path:
        # Try different possible logo file names
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'static', 'images', 'saryu-parivaar-logo.png'),
            os.path.join(settings.BASE_DIR, 'static', 'images', 'Saryu_Pariwar_Logo.jpeg'),
            os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png'),
            os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.jpeg'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logo_path = path
                break
    
    if not logo_path or not os.path.exists(logo_path):
        print(f"❌ Logo image not found.")
        print("Please provide the logo image file path.")
        print("Expected locations:")
        for path in possible_paths:
            print(f"  - {path}")
        return False
    
    # Read the image file
    try:
        with open(logo_path, 'rb') as f:
            file_content = f.read()
        print(f"✅ Read logo image: {len(file_content)} bytes")
        print(f"   File: {logo_path}")
    except Exception as e:
        print(f"❌ Error reading logo image: {e}")
        return False
    
    # Determine file extension and S3 key
    file_ext = os.path.splitext(logo_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg']:
        s3_key = f'media/saryu-parivaar-logo{file_ext}'
    else:
        s3_key = 'media/saryu-parivaar-logo.png'  # Default to PNG
    
    # S3 bucket
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # Check if file already exists
    if check_s3_object_exists(bucket_name, s3_key):
        print(f"⚠️  File already exists in S3: {s3_key}")
        print("   Auto-overwriting with new logo...")
        # Auto-overwrite for script execution
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(logo_path)
    if not content_type:
        if file_ext == '.png':
            content_type = 'image/png'
        elif file_ext in ['.jpg', '.jpeg']:
            content_type = 'image/jpeg'
        else:
            content_type = 'image/png'  # Default
    
    print(f"📤 Uploading logo to S3...")
    print(f"   Bucket: {bucket_name}")
    print(f"   Key: {s3_key}")
    print(f"   Content-Type: {content_type}")
    
    # Upload to S3
    success = upload_to_s3(file_content, bucket_name, s3_key, content_type)
    
    if success:
        print(f"✅ Successfully uploaded logo to S3!")
        print(f"   URL: /media/saryu-parivaar-logo{file_ext}")
        print(f"   Full S3 path: s3://{bucket_name}/{s3_key}")
        return True
    else:
        print(f"❌ Failed to upload logo to S3")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Logo Upload to S3")
    print("=" * 60)
    
    # Check S3 client
    s3_client = get_s3_client()
    if not s3_client:
        print("❌ Failed to create S3 client. Check AWS credentials in pod.env")
        sys.exit(1)
    
    print("✅ S3 client created successfully")
    print()
    
    # Check for logo file argument
    logo_path = None
    if len(sys.argv) > 1:
        logo_path = sys.argv[1]
        if not os.path.exists(logo_path):
            print(f"❌ Logo file not found: {logo_path}")
            sys.exit(1)
    
    # Upload logo
    success = upload_logo(logo_path)
    
    if success:
        print()
        print("=" * 60)
        print("✅ Upload Complete!")
        print("=" * 60)
        print("Next steps:")
        print("1. Update templates to use: /media/saryu-parivaar-logo.png (or .jpeg)")
        print("2. The logo will be served through Django view from S3")
    else:
        print()
        print("=" * 60)
        print("❌ Upload Failed")
        print("=" * 60)
        sys.exit(1)

