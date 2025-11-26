# S3 Image Configuration

## Overview
All images and media files are now configured to be fetched from the S3 bucket: **eicaws-saryupariwar**

## Configuration Details

### S3 Bucket
- **Bucket Name**: `eicaws-saryupariwar`
- **Region**: `ap-south-1`
- **Media URL Format**: `https://eicaws-saryupariwar.s3.amazonaws.com/media/[file_path]`

### Storage Backend
- **Storage Class**: `Saryupari_Brahmin_Project.storages.MediaStorage`
- **Location**: `media/`
- **ACL**: `public-read` (files are publicly accessible)
- **Query String Auth**: Disabled (clean URLs)

### Settings
The application automatically uses S3 storage when AWS credentials are configured in `pod.env`:
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`

## How It Works

### Image URLs in Templates
All image fields in Django models automatically generate S3 URLs when accessed via `.url`:

```django
<!-- Gallery Images -->
<img src="{{samaj_gallery_image.image.url}}">

<!-- Promotions -->
<img src="{{promotion.banner.url}}">

<!-- Testimonials -->
<img src="{{testimonial.image.url}}">

<!-- User Profile Pics -->
<img src="{{user.profile_pic.url}}">

<!-- Marriage Profile Pics -->
<img src="{{profile.marriage_profile_pic.url}}">
```

### Automatic S3 URL Generation
When you access any `ImageField` or `FileField` in templates or code using `.url`, Django automatically:
1. Checks the storage backend (S3 in this case)
2. Generates the full S3 URL: `https://eicaws-saryupariwar.s3.amazonaws.com/media/[file_path]`
3. Returns the URL for use in templates

### New Uploads
When users upload new images:
1. Files are uploaded to S3 bucket: `eicaws-saryupariwar`
2. Stored in the `media/` folder within the bucket
3. URLs are automatically generated pointing to S3

## Image Types Configured

### Homepage Images
- **Samaj Gallery Images**: Carousel slider images
- **Promotions**: Banner images in promotions section
- **Testimonials**: User testimonial images

### User Images
- **Profile Pictures**: User profile photos
- **Marriage Profile Pics**: Candidate profile pictures

### Other Media
- **Payment Proofs**: Payment transaction screenshots
- **Any other uploaded files**: All stored in S3

## Verification

To verify S3 configuration is working:

```bash
python test_s3_images.py
```

This script will:
- Test S3 connection
- Verify URL format
- List sample image URLs from database
- Show which images are accessible

## Troubleshooting

### Images Not Loading
1. **Check S3 Bucket Permissions**: Ensure bucket has public read access
2. **Verify AWS Credentials**: Check `pod.env` file has correct credentials
3. **Check CORS Settings**: Ensure S3 bucket allows requests from your domain
4. **Verify File Paths**: Ensure image paths in database match files in S3

### Access Denied Errors
- Verify AWS credentials have read/write permissions to the bucket
- Check bucket policy allows public read access for media files
- Ensure IAM user has `s3:GetObject` permission

### URL Generation Issues
- Verify `DEFAULT_FILE_STORAGE` is set to `Saryupari_Brahmin_Project.storages.MediaStorage`
- Check `MEDIA_URL` starts with `https://`
- Ensure `AWS_S3_CUSTOM_DOMAIN` is correctly set

## Current Status

✅ **S3 Storage Configured**: All media files use S3 bucket `eicaws-saryupariwar`
✅ **URL Generation**: All image URLs automatically point to S3
✅ **Public Access**: Files are set to `public-read` ACL
✅ **Templates Updated**: All image references use `.url` which generates S3 URLs

## Next Steps

1. **Test Image Loading**: Visit the homepage and verify images load from S3
2. **Upload Test**: Upload a new image and verify it's stored in S3
3. **Check Browser Console**: Verify no 404 errors for image URLs
4. **Verify S3 Bucket**: Check that files exist in `eicaws-saryupariwar/media/` folder

