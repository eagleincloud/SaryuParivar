# 502 Bad Gateway Error - FIXED

## Issue
The website was showing "502 Bad Gateway" error because Gunicorn was not running.

## Root Cause
- Gunicorn process was terminated (SIGTERM signal received)
- Nginx was trying to connect to `127.0.0.1:8000` but Gunicorn wasn't listening
- Error in nginx logs: `connect() failed (111: Connection refused)`

## Solution Applied

### 1. Checked Gunicorn Status
- Verified Gunicorn was not running
- Checked error logs to understand why it stopped

### 2. Restarted Gunicorn
```bash
cd /home/ec2-user/Saryu_Pariwar_Web_App
source venv/bin/activate
gunicorn Saryupari_Brahmin_Project.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile /tmp/gunicorn_access.log \
  --error-logfile /tmp/gunicorn_error.log \
  --daemon
```

### 3. Verified Connection
- Tested localhost connection to Gunicorn
- Verified nginx can now connect to Gunicorn
- Website should now be accessible

## Status
✅ **FIXED** - Gunicorn is now running and website should be accessible

## Verification
- **Website**: https://saryuparivar.com/
- **Status**: Should return HTTP 200 (not 502)

## If Issue Persists

1. **Check Gunicorn is running**:
   ```bash
   ssh -i /path/to/key.pem ec2-user@44.201.152.56
   ps aux | grep gunicorn
   ```

2. **Check Gunicorn logs**:
   ```bash
   tail -f /tmp/gunicorn_error.log
   ```

3. **Check nginx logs**:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

4. **Restart Gunicorn manually**:
   ```bash
   cd /home/ec2-user/Saryu_Pariwar_Web_App
   source venv/bin/activate
   pkill -f gunicorn
   gunicorn Saryupari_Brahmin_Project.wsgi:application \
     --bind 127.0.0.1:8000 \
     --workers 4 \
     --timeout 120 \
     --access-logfile /tmp/gunicorn_access.log \
     --error-logfile /tmp/gunicorn_error.log \
     --daemon
   ```

## Prevention

To prevent this in the future, consider:
1. Setting up Gunicorn as a systemd service (more reliable)
2. Adding monitoring/auto-restart for Gunicorn
3. Setting up health checks

---

**Issue resolved! Website should now be accessible.**

