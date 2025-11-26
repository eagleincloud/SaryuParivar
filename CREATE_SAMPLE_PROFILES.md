# Create Sample Profiles

## Issue
No profiles are showing because the database is empty. Users need to create their matrimonial profiles first.

## Solution

### Option 1: Users Create Their Own Profiles
Users can create profiles by:
1. Going to `/dashboard/my_profile/`
2. Filling out the profile form
3. Submitting the form

### Option 2: Create Sample Profiles (For Testing)

Run this script to create sample profiles:

```python
python manage.py shell
```

Then run:

```python
from dashboard.models import CandidateProfile
from administration.models import CustomUser
from datetime import date, time

# Create sample profiles
users = CustomUser.objects.filter(is_superuser=False)[:5]

for i, user in enumerate(users):
    if not hasattr(user, 'candidateprofile'):
        profile = CandidateProfile.objects.create(
            user=user,
            candidate_name=f"{user.first_name} {user.last_name}",
            gender='Male' if i % 2 == 0 else 'Female',
            height='5.8',
            color='Fair',
            education='Graduate',
            occupation='Engineer',
            annual_income='500000',
            father_name=user.father_name or 'Father Name',
            date_of_birth=date(1990 + i, 1, 1),
            age=34 - i,
            birth_place='City',
            father_or_guardian_occupation='Business',
            city='Mumbai',
            current_address='Sample Address',
            phone_number=user.phone_number,
            marriage_profile_pic=user.profile_pic if user.profile_pic else None
        )
        print(f"Created profile for {user.show_username()}")
```

## Changes Made

1. **Added empty state message** when no profiles exist
2. **Added default options** to filter dropdowns ("Select Gender", "Min", "Max")
3. **Filtered out None/empty values** from filter options
4. **Better handling** of empty database

## Status
✅ Empty state message added
✅ Filter dropdowns handle empty data
✅ Profiles will show once created

