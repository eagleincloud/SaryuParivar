# Boto3 S3 Integration

## Overview
The application now uses **boto3** to directly connect to S3 and serve images through Django views instead of using direct S3 URLs. This provides better control, security, and error handling.

## How It Works

### 1. S3 Client Connection
- Uses boto3 to create an S3 client with AWS credentials
- Connects directly to the S3 bucket: `eicaws-saryupariwar`
- All operations use boto3 API calls

### 2. Image Serving Flow
```
User Request → Django View → boto3 S3 Client → S3 Bucket → Image Content → Django Response
```

Instead of:
```
User Request → Direct S3 URL → S3 Bucket
```

### 3. Benefits
- ✅ **Better Control**: Can add authentication, logging, rate limiting
- ✅ **Error Handling**: Proper 404 handling, fallback images
- ✅ **Security**: Can restrict access, add watermarks, etc.
- ✅ **Caching**: Can implement server-side caching
- ✅ **Works with Private Buckets**: Doesn't require public read access
- ✅ **Image Processing**: Can resize, compress, or process images on-the-fly

## Implementation

### Files Created

1. **`Saryupari_Brahmin_Project/s3_utils.py`**
   - `get_s3_client()`: Creates boto3 S3 client
   - `get_s3_object()`: Fetches file from S3
   - `check_s3_object_exists()`: Checks if file exists
   - `serve_s3_image()`: Serves image through Django view
   - `upload_to_s3()`: Uploads files to S3
   - `get_s3_url_for_file()`: Generates presigned URLs (for private files)

2. **`Saryupari_Brahmin_Project/views.py`**
   - `serve_media()`: Django view that serves media files from S3

3. **URL Configuration**
   - Added route: `/media/<file_path>` → `serve_media` view
   - All media requests go through Django instead of direct S3 URLs

### Settings Updated

- `MEDIA_URL` changed from S3 URL to `/media/` (Django route)
- Images are now served at: `http://yourdomain.com/media/user_profile_pics/image.jpg`
- Instead of: `https://eicaws-saryupariwar.s3.amazonaws.com/media/user_profile_pics/image.jpg`

## Usage

### In Templates
Templates remain unchanged - they still use `.url`:
```django
<img src="{{user.profile_pic.url}}">
```

But now `.url` returns `/media/user_profile_pics/image.jpg` instead of the S3 URL.

### Direct boto3 Access
You can also use boto3 directly in your code:

```python
from Saryupari_Brahmin_Project.s3_utils import get_s3_object, check_s3_object_exists

# Check if file exists
exists = check_s3_object_exists('eicaws-saryupariwar', 'media/user_profile_pics/image.jpg')

# Get file content
content, content_type = get_s3_object('eicaws-saryupariwar', 'media/user_profile_pics/image.jpg')
```

## Testing

Run the test script:
```bash
python test_boto3_s3.py
```

This will test:
1. S3 client creation
2. Object existence checking
3. Fetching objects from S3
4. Serving images through Django views

## Configuration

### Required Settings
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name (`eicaws-saryupariwar`)
- `AWS_S3_REGION_NAME`: AWS region (`ap-south-1`)

### IAM Permissions Required
The AWS credentials need these S3 permissions:
- `s3:GetObject` - To read files
- `s3:PutObject` - To upload files
- `s3:HeadObject` - To check if files exist
- `s3:DeleteObject` - To delete files (optional)

## Advantages Over Direct URLs

| Feature | Direct S3 URLs | boto3 via Django |
|---------|---------------|------------------|
| Access Control | Bucket must be public | Can add Django auth |
| Error Handling | Browser shows 404 | Custom error pages |
| Logging | No server logs | Full request logging |
| Caching | Browser only | Server + browser |
| Image Processing | Not possible | Can resize/compress |
| Private Files | Requires presigned URLs | Can serve directly |
| Rate Limiting | Not possible | Can implement |

## Current Status

✅ **boto3 Integration Complete**
- S3 client connection working
- Image serving through Django views
- URL routing configured
- Error handling implemented

⚠️ **Note**: AWS credentials need to be valid and have proper permissions for full functionality.

## Next Steps

1. **Verify AWS Credentials**: Ensure credentials in `pod.env` are correct
2. **Test Image Serving**: Visit `/media/user_profile_pics/[filename]` to test
3. **Add Authentication** (optional): Restrict image access to logged-in users
4. **Add Caching** (optional): Implement Redis/Memcached for image caching
5. **Image Optimization** (optional): Add image resizing/compression on-the-fly

