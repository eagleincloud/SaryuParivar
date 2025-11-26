"""
SMS Service for sending OTP
Supports multiple SMS providers: MSG91, TextLocal, Fast2SMS, or custom API
"""
import requests
import os
from django.conf import settings

class SMSService:
    """
    SMS Service that can work with multiple providers
    Currently supports: MSG91, TextLocal, Fast2SMS, or simple HTTP API
    """
    
    @staticmethod
    def send_otp(phone_number, otp_code):
        """
        Send OTP via SMS
        Returns: (success: bool, message: str)
        """
        # Get SMS provider from settings (default: 'console' for testing)
        sms_provider = getattr(settings, 'SMS_PROVIDER', 'console')
        
        # Format phone number (add country code if needed)
        formatted_phone = phone_number
        if not formatted_phone.startswith('+91'):
            formatted_phone = f"+91{formatted_phone}"
        
        try:
            if sms_provider == 'msg91':
                return SMSService._send_via_msg91(formatted_phone, otp_code)
            elif sms_provider == 'textlocal':
                return SMSService._send_via_textlocal(formatted_phone, otp_code)
            elif sms_provider == 'fast2sms':
                return SMSService._send_via_fast2sms(formatted_phone, otp_code)
            elif sms_provider == 'custom_api':
                return SMSService._send_via_custom_api(formatted_phone, otp_code)
            else:
                # Default: console output (for testing/development)
                return SMSService._send_via_console(phone_number, otp_code)
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False, str(e)
    
    @staticmethod
    def _send_via_console(phone_number, otp_code):
        """Print OTP to console (for development/testing)"""
        print(f"\n{'='*50}")
        print(f"📱 OTP for {phone_number}: {otp_code}")
        print(f"{'='*50}\n")
        return True, "OTP sent (check console)"
    
    @staticmethod
    def _send_via_msg91(phone_number, otp_code):
        """Send OTP via MSG91"""
        api_key = getattr(settings, 'MSG91_API_KEY', '')
        sender_id = getattr(settings, 'MSG91_SENDER_ID', 'SARYUP')
        template_id = getattr(settings, 'MSG91_TEMPLATE_ID', '')
        
        if not api_key:
            return False, "MSG91 API key not configured"
        
        url = "https://control.msg91.com/api/v5/flow/"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authkey": api_key
        }
        
        # MSG91 Flow API
        payload = {
            "template_id": template_id,
            "sender": sender_id,
            "short_url": "0",
            "mobiles": phone_number,
            "otp": otp_code
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return True, "OTP sent successfully"
            else:
                return False, f"MSG91 API error: {response.text}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def _send_via_textlocal(phone_number, otp_code):
        """Send OTP via TextLocal"""
        api_key = getattr(settings, 'TEXTLOCAL_API_KEY', '')
        sender_id = getattr(settings, 'TEXTLOCAL_SENDER_ID', 'TXTLCL')
        
        if not api_key:
            return False, "TextLocal API key not configured"
        
        url = "https://api.textlocal.in/send/"
        payload = {
            'apikey': api_key,
            'numbers': phone_number,
            'message': f'Your OTP for Saryu Parivar login is {otp_code}. Valid for 5 minutes.',
            'sender': sender_id
        }
        
        try:
            response = requests.post(url, data=payload, timeout=10)
            result = response.json()
            if result.get('status') == 'success':
                return True, "OTP sent successfully"
            else:
                return False, f"TextLocal error: {result.get('errors', [{}])[0].get('message', 'Unknown error')}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def _send_via_fast2sms(phone_number, otp_code):
        """Send OTP via Fast2SMS"""
        api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
        
        if not api_key:
            return False, "Fast2SMS API key not configured"
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        headers = {
            'authorization': api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "route": "otp",
            "variables_values": otp_code,
            "numbers": phone_number.replace('+91', ''),
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            result = response.json()
            if result.get('return') == True:
                return True, "OTP sent successfully"
            else:
                return False, f"Fast2SMS error: {result.get('message', 'Unknown error')}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def _send_via_custom_api(phone_number, otp_code):
        """Send OTP via custom HTTP API"""
        api_url = getattr(settings, 'CUSTOM_SMS_API_URL', '')
        api_method = getattr(settings, 'CUSTOM_SMS_API_METHOD', 'POST').upper()
        api_headers = getattr(settings, 'CUSTOM_SMS_API_HEADERS', {})
        api_payload_template = getattr(settings, 'CUSTOM_SMS_API_PAYLOAD', {})
        
        if not api_url:
            return False, "Custom SMS API URL not configured"
        
        # Replace placeholders in payload
        payload = {}
        for key, value in api_payload_template.items():
            if isinstance(value, str):
                payload[key] = value.replace('{phone}', phone_number).replace('{otp}', otp_code)
            else:
                payload[key] = value
        
        try:
            if api_method == 'GET':
                response = requests.get(api_url, params=payload, headers=api_headers, timeout=10)
            else:
                response = requests.post(api_url, json=payload, headers=api_headers, timeout=10)
            
            if response.status_code in [200, 201]:
                return True, "OTP sent successfully"
            else:
                return False, f"API error: {response.text}"
        except Exception as e:
            return False, f"Error: {str(e)}"

