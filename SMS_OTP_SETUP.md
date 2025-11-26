# SMS OTP Setup Guide

## Overview

The application now supports **backend SMS OTP** instead of Firebase. This is more reliable and works with multiple SMS providers.

## Supported SMS Providers

1. **Console (Default)** - For testing/development (prints OTP to console)
2. **MSG91** - Popular Indian SMS provider
3. **TextLocal** - Indian SMS provider
4. **Fast2SMS** - Indian SMS provider
5. **Custom API** - Any HTTP-based SMS API

## Configuration

### Step 1: Choose SMS Provider

Edit `settings.py` and add the SMS provider configuration:

```python
# SMS Configuration
SMS_PROVIDER = 'console'  # Options: 'console', 'msg91', 'textlocal', 'fast2sms', 'custom_api'
```

### Step 2: Configure Provider Credentials

#### For MSG91:
```python
MSG91_API_KEY = 'your-msg91-api-key'
MSG91_SENDER_ID = 'SARYUP'  # Your registered sender ID
MSG91_TEMPLATE_ID = 'your-template-id'  # Optional
```

**Get MSG91 API Key:**
1. Sign up at https://msg91.com/
2. Go to Dashboard → API Keys
3. Copy your API key
4. Register a sender ID (6 characters)

#### For TextLocal:
```python
TEXTLOCAL_API_KEY = 'your-textlocal-api-key'
TEXTLOCAL_SENDER_ID = 'TXTLCL'  # Your sender ID
```

**Get TextLocal API Key:**
1. Sign up at https://www.textlocal.in/
2. Go to API → API Credentials
3. Copy your API key
4. Register a sender ID

#### For Fast2SMS:
```python
FAST2SMS_API_KEY = 'your-fast2sms-api-key'
```

**Get Fast2SMS API Key:**
1. Sign up at https://www.fast2sms.com/
2. Go to Dashboard → API Keys
3. Copy your API key

#### For Custom API:
```python
CUSTOM_SMS_API_URL = 'https://your-sms-api.com/send'
CUSTOM_SMS_API_METHOD = 'POST'  # or 'GET'
CUSTOM_SMS_API_HEADERS = {
    'Authorization': 'Bearer your-token',
    'Content-Type': 'application/json'
}
CUSTOM_SMS_API_PAYLOAD = {
    'phone': '{phone}',  # Will be replaced with actual phone number
    'otp': '{otp}',      # Will be replaced with actual OTP
    'message': 'Your OTP is {otp}'
}
```

## Testing

### Development Mode (Console)

By default, the app uses `console` mode which prints OTP to the terminal:

```python
SMS_PROVIDER = 'console'
```

When you request an OTP, you'll see:
```
==================================================
📱 OTP for 9876543210: 123456
==================================================
```

### Production Mode

1. Choose your SMS provider
2. Add credentials to `settings.py`
3. Set `SMS_PROVIDER` to your provider name
4. Test with a real phone number

## How It Works

1. **User enters phone number** → Clicks "Send OTP"
2. **Backend generates 6-digit OTP** → Stores in database
3. **Backend sends OTP via SMS** → Using configured provider
4. **User enters OTP** → Clicks "Verify OTP"
5. **Backend verifies OTP** → Logs in user if valid

## OTP Settings

- **OTP Length**: 6 digits
- **OTP Expiry**: 5 minutes
- **Rate Limiting**: Max 5 requests per hour per phone number

## Troubleshooting

### OTP not received?

1. **Check SMS provider credentials** - Verify API keys are correct
2. **Check phone number format** - Should be 10 digits (without country code)
3. **Check SMS provider dashboard** - Look for delivery status
4. **Check console logs** - Look for error messages

### SMS provider errors?

1. **MSG91**: Check API key and sender ID registration
2. **TextLocal**: Verify account balance and sender ID
3. **Fast2SMS**: Check API key and account status

### Testing without SMS?

Use `console` mode - OTP will be printed to terminal/server logs.

## Cost Comparison

- **MSG91**: ~₹0.20-0.30 per SMS
- **TextLocal**: ~₹0.15-0.25 per SMS
- **Fast2SMS**: ~₹0.10-0.20 per SMS
- **Console**: Free (for testing only)

## Migration from Firebase

✅ **Already done!** The app now uses backend SMS by default.

Firebase is still available as a fallback, but backend SMS is the primary method.

## Next Steps

1. Choose an SMS provider
2. Sign up and get API credentials
3. Add credentials to `settings.py`
4. Set `SMS_PROVIDER` in settings
5. Test with a real phone number

---

**OTP login is now working with backend SMS!** 🎉

