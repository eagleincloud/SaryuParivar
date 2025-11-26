# S3 Upload Error Fix

## Problem
**Error**: `ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden`

This error occurred when registering a new user with a profile picture. The S3 storage backend was trying to check if a file exists using `head_object`, but the AWS credentials didn't have the necessary permissions.

## Solution

### 1. Use Local Storage for Uploads in Development
- **Development mode**: Files are saved locally to `media/` directory
- **Production mode**: Files are saved to S3
- This prevents permission errors during development

### 2. Enhanced Error Handling in S3 Storage
- Added graceful error handling in `MediaStorage.exists()`
- If 403 error occurs, assumes file doesn't exist and allows upload
- Prevents crashes from permission issues

## Changes Made

### `Saryupari_Brahmin_Project/settings.py`
- Added check for `ENV == 'Local'` to use local storage in development
- Local storage used for uploads in development
- S3 still used for reading existing images (via boto3 views)

### `Saryupari_Brahmin_Project/storages.py`
- Added error handling in `exists()` method
- Handles 403 Forbidden errors gracefully
- Allows uploads even if read permissions are missing

## Current Configuration

**Development Mode** (ENV=Local):
- ✅ File uploads: Local storage (`media/` directory)
- ✅ Existing images: Read from S3 (via boto3 views)
- ✅ No S3 permission errors

**Production Mode** (ENV=Production):
- ✅ File uploads: S3 storage
- ✅ Existing images: S3 storage
- ✅ Full S3 integration

## Testing

1. **Register a new user**:
   - Go to: http://127.0.0.1:8000/
   - Click "Register"
   - Fill form and upload profile picture
   - ✅ Should work without 403 error

2. **Check file location**:
   - Uploaded files saved to: `media/user_profile_pics/`
   - Can be accessed at: `/media/user_profile_pics/[filename]`

3. **Verify**:
   - User registration works
   - Profile picture uploads successfully
   - No S3 permission errors

## File Locations

**Local Uploads** (Development):
- Profile pictures: `media/user_profile_pics/`
- Payment proofs: `media/payment_proofs/`
- Gallery images: `media/samaj_gallery/`

**S3 Images** (Existing):
- Still read from S3 bucket: `eicaws-saryupariwar`
- Served via Django views using boto3
- URLs: `/media/[path]`

## Production Deployment

When deploying to production:
1. Set `ENV=Production` in environment variables
2. Ensure AWS credentials have proper S3 permissions:
   - `s3:PutObject` - For uploading files
   - `s3:GetObject` - For reading files
   - `s3:HeadObject` - For checking file existence
   - `s3:DeleteObject` - For deleting files (optional)
3. Files will be uploaded directly to S3

## AWS Permissions Required

For production S3 uploads, ensure IAM user/role has:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:HeadObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::eicaws-saryupariwar/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::eicaws-saryupariwar"
    }
  ]
}
```

## Status

✅ **Fixed**: Registration with profile picture now works
✅ **Local Storage**: Used for uploads in development
✅ **Error Handling**: Graceful handling of S3 permission errors
✅ **Production Ready**: Can switch to S3 in production

---

**The registration error is now fixed!** 🎉

