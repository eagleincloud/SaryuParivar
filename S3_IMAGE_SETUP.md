# S3 Image Setup Guide

## Overview
All images are now configured to point directly to S3 bucket: `s3://eicaws-saryupariwar/media/`

## Current Status

✅ **Database entries created** pointing to S3 images
✅ **Paths fixed** to remove duplicate "media/" prefix
✅ **URLs configured** to load from S3

## Image Structure in S3

```
s3://eicaws-saryupariwar/media/
├── samaj_gallery/
│   ├── samaj_image_1.jpg
│   ├── samaj_image_2.jpg
│   ├── image_9.jpg
│   ├── image_10.jpg
│   ├── image_11.jpg
│   └── image_12.jpg
├── testimonials/
│   ├── surendra_dubey.jpg
│   ├── aditya_tiwari.jpg
│   └── dheeraj_shukla.jpg
└── promotions/
    ├── promotion_1.jpg
    └── promotion_2.jpg
```

## How It Works

1. **Database stores relative paths** (e.g., `samaj_gallery/image_9.jpg`)
2. **Django storage backend** adds `media/` prefix automatically
3. **Final S3 URL**: `https://eicaws-saryupariwar.s3.amazonaws.com/media/samaj_gallery/image_9.jpg`

## Scripts Available

### 1. `fetch_s3_images_v2.py`
- Creates database entries for common image paths
- Works even without S3 access (uses manual paths)
- Run: `python fetch_s3_images_v2.py`

### 2. `list_all_s3_images.py`
- Lists ALL images from S3 bucket (requires valid AWS credentials)
- Automatically creates database entries
- Run: `python list_all_s3_images.py`

### 3. `update_s3_paths.py`
- Fixes existing paths (removes duplicate "media/" prefix)
- Run: `python update_s3_paths.py`

## To List All Images from S3

If you have valid AWS credentials:

```bash
# Option 1: Using AWS CLI
aws s3 ls s3://eicaws-saryupariwar/media/ --recursive

# Option 2: Using Python script
python list_all_s3_images.py
```

## Adding New Images

### Method 1: Via Django Admin
1. Go to `/admin/`
2. Navigate to:
   - Administration → Samaj Galleries
   - Administration → Promotions
   - Administration → Testimonials
3. Upload images (they'll be stored in S3)

### Method 2: Direct S3 Upload
1. Upload images to S3 bucket at appropriate paths
2. Run `list_all_s3_images.py` to create database entries

### Method 3: Manual Database Entry
1. Upload image to S3
2. Create database entry with correct path (without "media/" prefix)

## Image URLs

All images are served from:
```
https://eicaws-saryupariwar.s3.amazonaws.com/media/[path]
```

Example:
- Gallery: `https://eicaws-saryupariwar.s3.amazonaws.com/media/samaj_gallery/image_9.jpg`
- Testimonial: `https://eicaws-saryupariwar.s3.amazonaws.com/media/testimonials/surendra_dubey.jpg`
- Promotion: `https://eicaws-saryupariwar.s3.amazonaws.com/media/promotions/promotion_1.jpg`

## Troubleshooting

### Images Not Showing
1. **Check S3 bucket permissions**: Ensure public read access
2. **Verify image paths**: Check database entries match S3 paths
3. **Check URLs**: Visit image URL directly in browser
4. **Verify credentials**: Ensure AWS credentials are correct

### Double "media/" in URL
- Run `python update_s3_paths.py` to fix paths

### Access Denied
- Update AWS credentials in `pod.env`
- Check IAM permissions for S3 access

## Current Database Entries

- **Gallery Images**: 11 entries
- **Promotions**: 4 entries  
- **Testimonials**: 3 entries

All pointing to S3 bucket paths!

