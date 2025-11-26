# Firebase Phone Authentication Setup Instructions

## Common Errors and Solutions

### Error: auth/billing-not-enabled

**This is the most common error.** Phone Authentication requires billing to be enabled on your Firebase project.

#### Solution: Enable Billing

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **saryuparivar-acc39**
3. Click on **⚙️ Project Settings** (gear icon in the left sidebar)
4. Go to **Usage and billing** tab
5. Click **Modify plan** or **Upgrade to Blaze plan**
6. Review the Blaze plan details:
   - **Pay-as-you-go**: You only pay for what you use
   - **Free tier**: Includes generous free quotas
   - **No monthly fees**: Only pay for usage beyond free tier
7. Click **Continue** or **Upgrade**
8. Add a payment method (credit card or debit card)
9. Complete the upgrade process
10. Wait a few minutes for billing to be activated

#### Important Notes:
- **Blaze plan is required** for Phone Authentication in production
- Free Spark plan has very limited SMS capabilities (only for testing)
- You only pay for SMS sent beyond the free tier
- Firebase provides free tier quotas that are usually sufficient for small to medium apps
- No charges until you exceed free tier limits

#### Free Tier Quotas (approximate):
- SMS messages: Limited (check Firebase Console for current limits)
- Phone verifications: Limited per month
- Additional usage is charged per SMS sent

### Error: auth/configuration-not-found

This error occurs when Phone Authentication is not enabled in your Firebase project. Follow these steps to enable it:

### Step 1: Go to Firebase Console
1. Visit: https://console.firebase.google.com/
2. Select your project: **saryuparivar-acc39**

### Step 2: Enable Billing (REQUIRED FIRST)
**⚠️ IMPORTANT: You must enable billing BEFORE enabling Phone Authentication**

1. Click on **⚙️ Project Settings** (gear icon)
2. Go to **Usage and billing** tab
3. Click **Modify plan** or **Upgrade to Blaze plan**
4. Add payment method and complete upgrade
5. Wait for billing activation (usually 1-2 minutes)

### Step 3: Enable Phone Authentication
1. In the left sidebar, click on **Authentication**
2. Click on **Sign-in method** tab
3. Find **Phone** in the list of providers
4. Click on **Phone** to open settings
5. Toggle **Enable** to ON
6. Click **Save**

### Step 4: Configure reCAPTCHA (if required)
1. Firebase will automatically set up reCAPTCHA verifier
2. For web apps, you may need to add your domain to authorized domains
3. Go to **Authentication > Settings > Authorized domains**
4. Make sure your domain is listed (localhost is included by default for development)

### Step 5: Test Phone Authentication
1. Go to **Authentication > Users** tab
2. Try sending a test OTP from your application
3. Check the browser console for any errors

### Step 6: Configure App Check (Optional but Recommended)
1. Go to **App Check** in Firebase Console
2. Register your app
3. This helps prevent abuse

### Important Notes:
- **Phone Authentication REQUIRES billing to be enabled** (Blaze plan)
- Free Spark plan does NOT support Phone Authentication (except very limited testing)
- Blaze plan is pay-as-you-go with generous free tier quotas
- You only pay for usage beyond the free tier
- Test phone numbers can be added in Firebase Console for testing without SMS charges
- Billing must be enabled BEFORE enabling Phone Authentication

### Testing Phone Numbers
You can add test phone numbers in Firebase Console:
1. Go to **Authentication > Sign-in method > Phone**
2. Scroll down to **Phone numbers for testing**
3. Add test numbers with verification codes
4. These work without sending actual SMS

### Troubleshooting:
- **Error: auth/billing-not-enabled**: ⚠️ **MOST COMMON** - Billing not enabled, upgrade to Blaze plan
- **Error: auth/configuration-not-found**: Phone Authentication not enabled in Firebase Console
- **Error: auth/invalid-phone-number**: Phone number format is incorrect
- **Error: auth/quota-exceeded**: SMS quota exceeded, check usage in Firebase Console
- **Error: auth/captcha-check-failed**: reCAPTCHA issue, refresh page
- **Error: auth/too-many-requests**: Too many OTP requests, wait before retrying

### Quick Fix Checklist:
1. ✅ Enable billing (Blaze plan) - **REQUIRED FIRST**
2. ✅ Enable Phone Authentication in Firebase Console
3. ✅ Add authorized domains if needed
4. ✅ Test with a real phone number or add test numbers

### Current Firebase Configuration:
- **Project ID**: saryuparivar-acc39
- **Auth Domain**: saryuparivar-acc39.firebaseapp.com
- **API Key**: AIzaSyBcOdG0hC3BCrhZkxrhxIzWdvc9wdWwHuA

