#!/usr/bin/env python
"""
Script to create sample matrimonial profiles for testing
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Saryupari_Brahmin_Project.settings')
django.setup()

from dashboard.models import CandidateProfile
from administration.models import CustomUser
from datetime import date, time
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_sample_profiles():
    """Create sample profiles for existing users"""
    users = CustomUser.objects.filter(is_superuser=False)
    
    if not users.exists():
        print("⚠️  No users found. Please register users first.")
        return
    
    sample_data = [
        {
            'gender': 'Male',
            'height': '5.8',
            'color': 'Fair',
            'education': 'Graduate',
            'occupation': 'Software Engineer',
            'annual_income': '800000',
            'city': 'Mumbai',
            'birth_place': 'Mumbai',
        },
        {
            'gender': 'Female',
            'height': '5.4',
            'color': 'Fair',
            'education': 'Post Graduate',
            'occupation': 'Doctor',
            'annual_income': '1200000',
            'city': 'Delhi',
            'birth_place': 'Delhi',
        },
        {
            'gender': 'Male',
            'height': '5.10',
            'color': 'Wheatish',
            'education': 'Graduate',
            'occupation': 'Business',
            'annual_income': '1500000',
            'city': 'Bangalore',
            'birth_place': 'Bangalore',
        },
        {
            'gender': 'Female',
            'height': '5.5',
            'color': 'Fair',
            'education': 'Graduate',
            'occupation': 'Teacher',
            'annual_income': '600000',
            'city': 'Pune',
            'birth_place': 'Pune',
        },
        {
            'gender': 'Male',
            'height': '5.9',
            'color': 'Wheatish',
            'education': 'Post Graduate',
            'occupation': 'Engineer',
            'annual_income': '1000000',
            'city': 'Hyderabad',
            'birth_place': 'Hyderabad',
        },
    ]
    
    created_count = 0
    for i, user in enumerate(users):
        # Skip if user already has a profile
        if hasattr(user, 'candidateprofile'):
            print(f"⏭️  User {user.show_username()} already has a profile")
            continue
        
        # Get sample data (cycle through if more users than samples)
        sample = sample_data[i % len(sample_data)]
        
        # Create a simple profile picture
        img = Image.new('RGB', (200, 200), color=(200, 200, 200))
        output = io.BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)
        profile_pic = ContentFile(output.read(), name=f'profile_{user.id}.jpg')
        
        try:
            profile = CandidateProfile.objects.create(
                user=user,
                candidate_name=f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username,
                gender=sample['gender'],
                height=sample['height'],
                color=sample['color'],
                education=sample['education'],
                occupation=sample['occupation'],
                annual_income=sample['annual_income'],
                father_name=user.father_name or f"{user.first_name}'s Father",
                date_of_birth=date(1990 + i, 1, 1),
                birth_place=sample['birth_place'],
                father_or_guardian_occupation='Business',
                city=sample['city'],
                current_address=f"{sample['city']}, India",
                phone_number=user.phone_number or f"999999999{i}",
                marriage_profile_pic=profile_pic
            )
            print(f"✅ Created profile for {user.show_username()}: {profile.candidate_name}")
            created_count += 1
        except Exception as e:
            print(f"❌ Error creating profile for {user.show_username()}: {str(e)}")
    
    print(f"\n✅ Created {created_count} profiles")
    print(f"📊 Total profiles in database: {CandidateProfile.objects.count()}")

if __name__ == '__main__':
    create_sample_profiles()

