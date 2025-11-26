"""
S3 Image serving views using boto3
"""
from django.http import Http404
from .s3_utils import serve_s3_image


def serve_media(request, file_path):
    """
    Serve media files from S3 using boto3
    
    URL pattern: /media/<file_path>
    Example: /media/user_profile_pics/image.jpg
    """
    try:
        return serve_s3_image(request, file_path)
    except Http404:
        raise
    except Exception as e:
        # Log error and return 404
        print(f"Error serving media file: {e}")
        raise Http404("File not found")

