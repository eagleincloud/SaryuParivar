"""
Firebase Authentication utility for OTP verification
"""
import json
import requests
from django.conf import settings
from Saryupari_Brahmin_Project.firebase_config import FIREBASE_CONFIG

def verify_firebase_id_token(id_token):
    """
    Verify Firebase ID token using Firebase REST API
    Returns user info if token is valid, None otherwise
    """
    try:
        verify_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={FIREBASE_CONFIG['apiKey']}"
        response = requests.post(verify_url, json={"idToken": id_token}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('users') and len(data['users']) > 0:
                user_info = data['users'][0]
                return {
                    'uid': user_info.get('localId'),
                    'phone_number': user_info.get('phoneNumber', ''),
                    'email': user_info.get('email', ''),
                }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error verifying Firebase token: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error verifying Firebase token: {e}")
        return None

