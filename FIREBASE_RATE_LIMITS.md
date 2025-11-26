# Firebase Phone Authentication Rate Limits

## Error: "Too many requests. Please try again later."

This error occurs when you've exceeded Firebase's rate limits for Phone Authentication.

## Understanding Rate Limits

Firebase has rate limits to prevent abuse and ensure service stability:

### Rate Limit Details:
- **Per phone number**: Limited requests per hour/day
- **Per IP address**: Limited requests from same IP
- **Per project**: Overall project limits
- **Cooldown period**: Usually 1-5 minutes between requests

### Typical Limits:
- **Same phone number**: ~5-10 requests per hour
- **Same IP**: ~20-30 requests per hour
- **Project-wide**: Varies based on plan

## Solutions

### 1. Wait and Retry
- **Wait 1-5 minutes** before trying again
- The application now shows a countdown timer
- Wait for the timer to complete before retrying

### 2. Use Different Phone Number (for testing)
- If testing, use different phone numbers
- Or use Firebase test phone numbers (no rate limits)

### 3. Check Firebase Console
- Go to Firebase Console → Authentication → Users
- Check if there are any blocked numbers
- Review usage statistics

### 4. Implement Exponential Backoff
- The application automatically handles retries
- Wait longer between attempts if rate limited

## Prevention Tips

### For Development:
1. **Use Test Phone Numbers**
   - Go to Authentication → Sign-in method → Phone
   - Add test numbers with verification codes
   - No rate limits on test numbers

2. **Space Out Requests**
   - Don't send multiple OTPs in quick succession
   - Wait at least 1 minute between attempts

3. **Use Different Numbers**
   - Test with different phone numbers
   - Avoid hammering the same number

### For Production:
1. **Implement Rate Limiting on Your Side**
   - Track OTP requests per user
   - Limit requests to 1 per minute per phone
   - Show clear error messages

2. **User Education**
   - Inform users about rate limits
   - Show countdown timers
   - Provide alternative contact methods

3. **Monitor Usage**
   - Track OTP request patterns
   - Identify abuse early
   - Set up alerts

## Firebase Test Phone Numbers

To avoid rate limits during development:

1. Go to **Firebase Console**
2. Navigate to **Authentication → Sign-in method → Phone**
3. Scroll to **Phone numbers for testing**
4. Click **Add phone number**
5. Enter:
   - **Phone number**: `+91 9999999999` (or any number)
   - **Verification code**: `123456` (or any 6-digit code)
6. Click **Save**

### Using Test Numbers:
- No SMS is sent
- No rate limits
- Use the exact verification code you set
- Works immediately

## Error Codes Related to Rate Limits

- `auth/too-many-requests`: Rate limit exceeded
- `auth/quota-exceeded`: Project quota exceeded (different from rate limit)
- `auth/operation-not-allowed`: Phone auth not enabled (different issue)

## Best Practices

1. **Always show retry timers** to users
2. **Cache verification attempts** to avoid duplicates
3. **Implement exponential backoff** for retries
4. **Monitor Firebase Console** for usage patterns
5. **Use test numbers** during development
6. **Educate users** about rate limits

## Contact Firebase Support

If you consistently hit rate limits:
1. Check your Firebase plan limits
2. Review usage in Firebase Console
3. Contact Firebase support if limits seem too restrictive
4. Consider upgrading plan if needed

---

**Remember**: Rate limits are there to protect the service. Be patient and wait for the cooldown period.

