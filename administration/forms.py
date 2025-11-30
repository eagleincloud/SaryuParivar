from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, SupportRequest
from PIL import Image
import io

class RegistrationForm(forms.ModelForm):
    form_type = forms.CharField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        min_length=8,
        help_text='Password must be at least 8 characters long.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label='Confirm Password'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text='Required for password reset.'
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'father_name', 'native_village', 'district', 'tehsil', 'current_address', 'phone_number', 'business_address', 'business_phone_number', 'profile_pic', 'email']
        widgets = {
            'profile_pic': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control',
                'onchange': 'compressImage(this)'
            })
        }
    
    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            # Check file size (max 5MB)
            if profile_pic.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large (max 5MB). Please upload a smaller image.')
            
            # Compress and resize image
            try:
                # Open and process image
                img = Image.open(profile_pic)
                
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if image is too large (max 800x800)
                max_size = 800
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Save compressed image to BytesIO
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Replace the file with compressed version
                from django.core.files.base import ContentFile
                from django.core.files.uploadedfile import InMemoryUploadedFile
                import os
                
                # Get original filename
                filename = profile_pic.name
                if '.' in filename:
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}.jpg"
                else:
                    filename = f"{filename}.jpg"
                
                # Create new file object
                profile_pic.file = ContentFile(output.read())
                profile_pic.name = filename
                profile_pic.size = output.tell()
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise forms.ValidationError(f'Error processing image: {str(e)}')
        
        return profile_pic
    
    def clean(self):
        errors = []
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        business_phone_number = cleaned_data.get("business_phone_number")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm:
            if password != password_confirm:
                errors.append('Passwords do not match')
        
        if len(errors) != 0:
            raise forms.ValidationError(errors)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form that validates email matches registration email"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update email field styling
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your registered email address'
        })
        self.fields['email'].label = 'Email Address'
        self.fields['email'].help_text = 'Enter the email address you used during registration'
    
    def clean_email(self):
        """Validate that the email exists and was used during registration"""
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter your email address')
        
        # Check if user exists with this email
        try:
            user = CustomUser.objects.get(email=email, is_active=True)
            # Email exists and user is active - valid
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(
                'No account found with this email address. Please check your email or register first.'
            )
        except CustomUser.MultipleObjectsReturned:
            # Multiple users with same email (shouldn't happen, but handle it)
            return email
    
    def get_users(self, email):
        """Override to find users by email and validate it matches registration email"""
        if not email:
            return []
        
        # Find users with this exact email (case-insensitive)
        users = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True
        )
        
        # Return only users whose email exactly matches (case-sensitive check)
        users_list = []
        for user in users:
            if user.email.lower() == email.lower():
                users_list.append(user)
        
        return users_list


class SupportForm(forms.ModelForm):
    """Form for user support requests"""
    
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What can we help you with?',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your issue or question in detail...',
                'rows': 5,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill user information if logged in
        if self.user and self.user.is_authenticated:
            if not self.initial.get('name'):
                self.initial['name'] = self.user.get_full_name() or self.user.show_username()
            if not self.initial.get('email'):
                self.initial['email'] = self.user.email or ''
            if not self.initial.get('phone_number'):
                self.initial['phone_number'] = str(self.user.phone_number) if self.user.phone_number else ''
