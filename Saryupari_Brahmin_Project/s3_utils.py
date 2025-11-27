"""
S3 Utilities using boto3 for direct S3 access
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from django.conf import settings
from django.http import HttpResponse, Http404
from io import BytesIO


def get_s3_client():
    """
    Get configured S3 client using boto3
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        return s3_client
    except (NoCredentialsError, AttributeError) as e:
        print(f"Error creating S3 client: {e}")
        return None


def get_s3_object(bucket_name, key):
    """
    Fetch an object from S3 using boto3
    
    Args:
        bucket_name: S3 bucket name
        key: S3 object key (file path)
    
    Returns:
        tuple: (content, content_type) or (None, None) if error
    """
    s3_client = get_s3_client()
    if not s3_client:
        return None, None
    
    try:
        # Get object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        
        # Read content
        content = response['Body'].read()
        
        # Get content type
        content_type = response.get('ContentType', 'application/octet-stream')
        
        return content, content_type
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f"File not found in S3: {key}")
        elif error_code == 'AccessDenied':
            print(f"Access denied to S3 object: {key}")
        else:
            print(f"Error fetching S3 object: {e}")
        return None, None
    
    except Exception as e:
        print(f"Unexpected error fetching S3 object: {e}")
        return None, None


def check_s3_object_exists(bucket_name, key):
    """
    Check if an object exists in S3
    
    Args:
        bucket_name: S3 bucket name
        key: S3 object key (file path)
    
    Returns:
        bool: True if object exists, False otherwise
    """
    s3_client = get_s3_client()
    if not s3_client:
        return False
    
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return False
        return False
    except Exception as e:
        print(f"Error checking S3 object: {e}")
        return False


def upload_to_s3(file_content, bucket_name, key, content_type=None):
    """
    Upload a file to S3 using boto3
    
    Args:
        file_content: File content (bytes or file-like object)
        bucket_name: S3 bucket name
        key: S3 object key (file path)
        content_type: MIME type of the file
    
    Returns:
        bool: True if successful, False otherwise
    """
    s3_client = get_s3_client()
    if not s3_client:
        return False
    
    try:
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        
        # Don't set ACL - bucket doesn't support ACLs (use bucket policy instead)
        # extra_args['ACL'] = 'public-read'
        
        s3_client.upload_fileobj(
            BytesIO(file_content) if isinstance(file_content, bytes) else file_content,
            bucket_name,
            key,
            ExtraArgs=extra_args if extra_args else None
        )
        return True
    
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False


def serve_s3_image(request, file_path):
    """
    Serve an image from S3 through Django view
    
    Args:
        request: Django request object
        file_path: Path to file in S3 (relative to media/ folder)
    
    Returns:
        HttpResponse with image content or 404
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if not bucket_name:
        raise Http404("S3 bucket not configured")
    
    # Construct S3 key (add 'media/' prefix if not present)
    # Django ImageField.name already includes the path relative to media/
    # So we need to check if it starts with 'media/' or not
    if file_path.startswith('media/'):
        s3_key = file_path
    elif '/' in file_path:  # Has subdirectory, add media/ prefix
        s3_key = f'media/{file_path}'
    else:  # Just filename, add media/ prefix
        s3_key = f'media/{file_path}'
    
    # Fetch from S3
    content, content_type = get_s3_object(bucket_name, s3_key)
    
    if content is None:
        raise Http404(f"Image not found: {s3_key}")
    
    # Create response with appropriate headers
    response = HttpResponse(content, content_type=content_type)
    
    # Add cache headers
    response['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
    response['Content-Disposition'] = f'inline; filename="{file_path.split("/")[-1]}"'
    
    return response


def get_s3_url_for_file(file_path, expires_in=3600):
    """
    Generate a presigned URL for S3 object (if needed for private files)
    
    Args:
        file_path: Path to file in S3
        expires_in: URL expiration time in seconds
    
    Returns:
        str: Presigned URL or None if error
    """
    s3_client = get_s3_client()
    if not s3_client:
        return None
    
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if not bucket_name:
        return None
    
    # Construct S3 key
    if file_path.startswith('media/'):
        s3_key = file_path
    else:
        s3_key = f'media/{file_path}'
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=expires_in
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

