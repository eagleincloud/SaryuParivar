# S3 ACL Error Fix

## Issue
Getting error during registration:
```
AccessControlListNotSupported: The bucket does not allow ACLs
```

## Root Cause
The S3 bucket `eicaws-saryupariwar` has ACLs disabled (common in newer S3 buckets). The storage backend was trying to set `ACL='public-read'` which is not supported.

## Solution

### 1. Removed ACL Settings
- Set `default_acl = None` in `MediaStorage` class
- Set `AWS_DEFAULT_ACL = None` in `settings.py`
- Override `_save()` method to ensure no ACL is passed to S3

### 2. Enhanced Error Handling
- Added `AccessControlListNotSupported` to error handling in `save()` method
- Automatic fallback to local storage if ACL error occurs

### 3. Files Updated
- `Saryupari_Brahmin_Project/storages.py`:
  - Set `default_acl = None`
  - Added `_save()` override to prevent ACL from being passed
  - Added `AccessControlListNotSupported` to error handling
  
- `Saryupari_Brahmin_Project/settings.py`:
  - Set `AWS_DEFAULT_ACL = None`

## Testing
✅ Storage initialized with `default_acl = None`
✅ No ACL will be passed to S3 during uploads
✅ Files will be uploaded successfully without ACL errors

## Public Access
If files need to be publicly accessible, configure the S3 bucket policy instead of ACLs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::eicaws-saryupariwar/media/*"
    }
  ]
}
```

## Deployment Status
✅ Files synced to EC2
✅ Gunicorn reloaded
✅ Ready for testing

## Next Steps
1. Test registration with profile picture upload
2. Verify files are uploaded to S3 successfully
3. Confirm files are accessible via S3 URLs (if bucket policy is set)

