#!/bin/bash
# Deployment script for EC2
# Usage: ./DEPLOY_TO_EC2.sh [path_to_ssh_key.pem]

EC2_IP="44.201.152.56"
EC2_USER="ec2-user"
EC2_PATH="/home/ec2-user/Saryu_Pariwar_Web_App"
SSH_KEY="${1:-~/.ssh/saryuparivar-key.pem}"

echo "=========================================="
echo "Deploying to EC2: $EC2_IP"
echo "=========================================="

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found at: $SSH_KEY"
    echo "Please provide the path to your SSH key:"
    echo "Usage: ./DEPLOY_TO_EC2.sh /path/to/key.pem"
    exit 1
fi

# Set correct permissions for SSH key
chmod 400 "$SSH_KEY"

echo "✅ SSH key found: $SSH_KEY"
echo ""

# Step 1: Sync files to EC2
echo "📦 Step 1: Syncing files to EC2..."
rsync -avz --exclude='.git' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='db.sqlite3' \
    --exclude='media/' \
    --exclude='.env' \
    --exclude='*.log' \
    -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    ./ $EC2_USER@$EC2_IP:$EC2_PATH/

if [ $? -eq 0 ]; then
    echo "✅ Files synced successfully"
else
    echo "❌ File sync failed"
    exit 1
fi

echo ""

# Step 2: Collect static files
echo "📦 Step 2: Collecting static files on EC2..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP << 'EOF'
cd /home/ec2-user/Saryu_Pariwar_Web_App
source venv/bin/activate
python manage.py collectstatic --noinput
EOF

if [ $? -eq 0 ]; then
    echo "✅ Static files collected"
else
    echo "❌ Static file collection failed"
    exit 1
fi

echo ""

# Step 3: Run migrations
echo "📦 Step 3: Running database migrations..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP << 'EOF'
cd /home/ec2-user/Saryu_Pariwar_Web_App
source venv/bin/activate
python manage.py migrate --noinput
EOF

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed"
else
    echo "❌ Migrations failed"
    exit 1
fi

echo ""

# Step 4: Restart Gunicorn
echo "📦 Step 4: Restarting Gunicorn..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP << 'EOF'
sudo systemctl restart gunicorn
sleep 2
sudo systemctl status gunicorn --no-pager | head -10
EOF

if [ $? -eq 0 ]; then
    echo "✅ Gunicorn restarted"
else
    echo "❌ Gunicorn restart failed"
    exit 1
fi

echo ""

# Step 5: Reload Nginx
echo "📦 Step 5: Reloading Nginx..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP << 'EOF'
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl status nginx --no-pager | head -10
EOF

if [ $? -eq 0 ]; then
    echo "✅ Nginx reloaded"
else
    echo "❌ Nginx reload failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "🌐 Website: https://saryuparivar.com"
echo "🌐 Direct IP: http://44.201.152.56"
echo ""
echo "Test the deployment:"
echo "  curl -I https://saryuparivar.com/"
echo ""

