#!/usr/bin/env python
"""Test S3 credentials from CSV file"""
import os
import boto3
from botocore.exceptions import ClientError

# Credentials should be set via environment variables or config file
# DO NOT commit actual credentials to git
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID', 'YOUR_AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'YOUR_AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = 'eicaws-saryupariwar'
REGION = 'ap-south-1'

print("🔍 Testing S3 connection with new credentials...")
print(f"Access Key: {ACCESS_KEY[:10]}...")
print(f"Bucket: {BUCKET_NAME}")
print(f"Region: {REGION}\n")

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
    
    # Test bucket access
    print("1. Testing bucket access...")
    s3.head_bucket(Bucket=BUCKET_NAME)
    print("   ✅ Bucket access successful!")
    
    # Test listing objects
    print("\n2. Testing object listing...")
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='media/', MaxKeys=5)
    if 'Contents' in response:
        print(f"   ✅ Found {len(response['Contents'])} objects (showing first 5)")
        for obj in response['Contents'][:5]:
            print(f"      - {obj['Key']} ({obj['Size']} bytes)")
    else:
        print("   ⚠️  No objects found in media/ prefix")
    
    # Test write permission (create a test file)
    print("\n3. Testing write permission...")
    test_key = 'media/test_upload.txt'
    test_content = b'Test upload from Django application'
    s3.put_object(Bucket=BUCKET_NAME, Key=test_key, Body=test_content)
    print("   ✅ Write permission successful!")
    
    # Clean up test file
    s3.delete_object(Bucket=BUCKET_NAME, Key=test_key)
    print("   ✅ Test file deleted")
    
    print("\n✅ All S3 tests passed! Credentials are valid and working.")
    
except ClientError as e:
    error_code = e.response.get('Error', {}).get('Code', '')
    error_msg = e.response.get('Error', {}).get('Message', str(e))
    print(f"\n❌ S3 Error ({error_code}): {error_msg}")
    if error_code == '403':
        print("   This indicates the credentials don't have sufficient permissions.")
    elif error_code == 'InvalidAccessKeyId':
        print("   The access key ID is invalid.")
    elif error_code == 'SignatureDoesNotMatch':
        print("   The secret access key is incorrect.")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

