# EC2 Deployment Instructions

## Quick Deploy

### Option 1: Using the Deployment Script (Recommended)

1. **Make sure you have the SSH key file:**
   ```bash
   # The key file should be named something like:
   # saryuparivar-key.pem or similar
   ```

2. **Run the deployment script:**
   ```bash
   cd /Users/adityatiwari/Downloads/SaryuParivarWebsite
   ./DEPLOY_TO_EC2.sh /path/to/your/key.pem
   ```

   If your key is in the default location:
   ```bash
   ./DEPLOY_TO_EC2.sh ~/.ssh/saryuparivar-key.pem
   ```

### Option 2: Manual Deployment

If you prefer to deploy manually, follow these steps:

#### Step 1: Sync Files to EC2

```bash
# Replace /path/to/key.pem with your actual SSH key path
rsync -avz --exclude='.git' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='db.sqlite3' \
    --exclude='media/' \
    --exclude='.env' \
    -e "ssh -i /path/to/key.pem -o StrictHostKeyChecking=no" \
    ./ ec2-user@44.201.152.56:/home/ec2-user/Saryu_Pariwar_Web_App/
```

#### Step 2: Collect Static Files

```bash
ssh -i /path/to/key.pem -o StrictHostKeyChecking=no ec2-user@44.201.152.56 << 'EOF'
cd /home/ec2-user/Saryu_Pariwar_Web_App
source venv/bin/activate
python manage.py collectstatic --noinput
EOF
```

#### Step 3: Run Migrations

```bash
ssh -i /path/to/key.pem -o StrictHostKeyChecking=no ec2-user@44.201.152.56 << 'EOF'
cd /home/ec2-user/Saryu_Pariwar_Web_App
source venv/bin/activate
python manage.py migrate --noinput
EOF
```

#### Step 4: Restart Gunicorn

```bash
ssh -i /path/to/key.pem -o StrictHostKeyChecking=no ec2-user@44.201.152.56 << 'EOF'
sudo systemctl restart gunicorn
sudo systemctl status gunicorn --no-pager | head -15
EOF
```

#### Step 5: Reload Nginx

```bash
ssh -i /path/to/key.pem -o StrictHostKeyChecking=no ec2-user@44.201.152.56 << 'EOF'
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl status nginx --no-pager | head -15
EOF
```

## What Gets Deployed

✅ **All template files** (including standardized sidebars)
✅ **All view files** (with print statements removed)
✅ **All model files** (including new migrations)
✅ **All static files** (collected via collectstatic)
✅ **Configuration files** (except .env which stays on server)

## Verification

After deployment, verify:

1. **Check website:**
   ```bash
   curl -I https://saryuparivar.com/
   # Should return HTTP 200
   ```

2. **Check DNS:**
   ```bash
   dig +short saryuparivar.com
   # Should return: 44.201.152.56
   ```

3. **Test pages:**
   - https://saryuparivar.com/
   - https://saryuparivar.com/dashboard/
   - https://saryuparivar.com/dashboard/user_profile/
   - https://saryuparivar.com/dashboard/shortlisted_profiles/

## Domain Configuration

The domain `saryuparivar.com` should already be pointing to `44.201.152.56`.

**To verify DNS:**
```bash
dig +short saryuparivar.com
# Should show: 44.201.152.56
```

**If DNS is not correct:**
1. Log in to your domain registrar
2. Update the A record for `saryuparivar.com` to point to `44.201.152.56`
3. Wait for DNS propagation (5-30 minutes)

## Troubleshooting

### SSH Connection Issues

If you get "Permission denied":
1. Check that your SSH key file has correct permissions:
   ```bash
   chmod 400 /path/to/key.pem
   ```

2. Verify the key file path is correct

3. If using a different key, update the path in the script

### Service Issues

**Check Gunicorn:**
```bash
ssh -i /path/to/key.pem ec2-user@44.201.152.56
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50
```

**Check Nginx:**
```bash
ssh -i /path/to/key.pem ec2-user@44.201.152.56
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

## Current Status

- **EC2 IP**: 44.201.152.56
- **Domain**: saryuparivar.com
- **DNS**: Should point to 44.201.152.56
- **Services**: Gunicorn + Nginx

## Changes Being Deployed

1. ✅ Standardized sidebars across all pages
2. ✅ Removed all debug print statements
3. ✅ Updated templates with sidebar includes
4. ✅ Fixed user_profile and shortlisted_profiles pages
5. ✅ All migrations included

