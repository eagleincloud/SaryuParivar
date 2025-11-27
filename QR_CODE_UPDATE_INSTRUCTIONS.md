# QR Code Update - Instructions

## ✅ New QR Code Uploaded to S3

The new QR code image has been uploaded to S3 and is now being served from:
- **S3 Location**: `s3://eicaws-saryupariwar/media/qr_code.jpeg`
- **URL**: `/media/qr_code.jpeg`
- **Template**: Updated to use S3 path

## 🔄 Browser Cache Issue

If you're still seeing the old QR code image, it's likely due to **browser caching**. Here's how to fix it:

### Option 1: Hard Refresh (Recommended)
- **Windows/Linux**: Press `Ctrl + F5` or `Ctrl + Shift + R`
- **Mac**: Press `Cmd + Shift + R`
- This forces the browser to reload the image from the server

### Option 2: Clear Browser Cache
1. Open browser settings
2. Clear browsing data/cache
3. Select "Cached images and files"
4. Clear data
5. Refresh the page

### Option 3: Incognito/Private Window
- Open the payment page in an incognito/private window
- This bypasses cache and shows the new image

## ✅ Verification

The new QR code is confirmed to be:
- ✅ Uploaded to S3 successfully
- ✅ Template updated to use `/media/qr_code.jpeg`
- ✅ Gunicorn restarted
- ✅ Served through Django's media view

## 📝 Note

The QR code image is now stored in S3 and served dynamically. To update it in the future:
1. Replace `static/images/qr_code.jpeg` with new image
2. Run the upload script on EC2
3. Clear browser cache to see the new image

