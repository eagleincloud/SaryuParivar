from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from botocore.exceptions import ClientError
import os

class MediaStorage(S3Boto3Storage):
    """
    Custom S3 storage for media files with fallback to local storage.
    All media files (images, uploads) are stored in S3 bucket: eicaws-saryupariwar
    
    This storage backend ensures all media files are fetched from and stored to S3.
    If S3 credentials are invalid, falls back to local storage.
    Images are accessible at: https://eicaws-saryupariwar.s3.amazonaws.com/media/[path]
    """
    location = 'media'
    file_overwrite = False
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    region_name = settings.AWS_S3_REGION_NAME
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    # ACLs are disabled on this bucket - use bucket policy for public access instead
    default_acl = None  # Don't set ACLs (bucket doesn't support them)
    querystring_auth = False  # Don't add authentication to URLs
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize fallback storage
        self._fallback_storage = None
        self._s3_available = self._check_s3_access()
    
    def _check_s3_access(self):
        """Check if S3 is accessible with current credentials"""
        try:
            # Try to access the bucket
            self.connection.meta.client.head_bucket(Bucket=self.bucket_name)
            return True
        except (ClientError, Exception) as e:
            error_code = ''
            if hasattr(e, 'response'):
                error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                print(f"⚠️  S3 access denied ({error_code}), falling back to local storage")
                return False
            # For other errors, assume S3 is available but might have issues
            return True
    
    def _get_fallback_storage(self):
        """Get local filesystem storage as fallback"""
        if self._fallback_storage is None:
            media_root = os.path.join(settings.BASE_DIR, 'media')
            os.makedirs(media_root, exist_ok=True)
            self._fallback_storage = FileSystemStorage(location=media_root)
        return self._fallback_storage
    
    def exists(self, name):
        """
        Override exists to handle permission errors gracefully.
        If we can't check existence (403 error), assume file doesn't exist and allow upload.
        """
        if not self._s3_available:
            return self._get_fallback_storage().exists(name)
        
        try:
            return super().exists(name)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                # Fall back to local storage check
                return self._get_fallback_storage().exists(name)
            # For other errors, re-raise
            raise
    
    def _save(self, name, content):
        """
        Override _save to ensure no ACL is passed (bucket doesn't support ACLs).
        """
        # Temporarily set default_acl to None to prevent ACL from being passed
        original_acl = self.default_acl
        self.default_acl = None
        
        try:
            # Call parent _save without ACL
            return super()._save(name, content)
        finally:
            # Restore original ACL setting
            self.default_acl = original_acl
    
    def save(self, name, content, max_length=None):
        """
        Save file to S3, or fallback to local storage if S3 is not available.
        """
        if not self._s3_available:
            # Use local storage
            return self._get_fallback_storage().save(name, content, max_length)
        
        try:
            # Save without ACLs (bucket doesn't support them)
            return super().save(name, content, max_length)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch', 'AccessDenied', 'AccessControlListNotSupported'):
                # Fall back to local storage
                print(f"⚠️  S3 upload failed ({error_code}), saving to local storage")
                self._s3_available = False  # Mark S3 as unavailable
                return self._get_fallback_storage().save(name, content, max_length)
            # For other errors, re-raise
            raise
    
    def open(self, name, mode='rb'):
        """Open file from S3, or fallback to local storage"""
        if not self._s3_available:
            return self._get_fallback_storage().open(name, mode)
        
        try:
            return super().open(name, mode)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch', 'NoSuchKey'):
                # Fall back to local storage
                return self._get_fallback_storage().open(name, mode)
            raise
    
    def url(self, name):
        """Get URL for file - try S3 first, then local"""
        if not self._s3_available:
            return self._get_fallback_storage().url(name)
        
        try:
            return super().url(name)
        except Exception:
            # Fall back to local URL
            return self._get_fallback_storage().url(name)
