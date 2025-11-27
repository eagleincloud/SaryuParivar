# Python Imports
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError

# Local Imports
from .mixins import FileDeleteMixin
from administration.models import CustomUser

class DateFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def validate_phone_number(value):
    if not isinstance(value, int):
        raise ValidationError('Phone must be an integer.')
    if len(str(abs(value))) != 10:
        raise ValidationError('Phone number must be exactly 10 digits.')


class MarriageProfile(DateFields):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    head_of_the_family_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    height_feet = models.PositiveIntegerField(blank=True, null=True)
    height_inches = models.PositiveIntegerField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    education = models.CharField(max_length=500)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    time_of_birth = models.TimeField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    gotra = models.CharField(max_length=100, blank=True, null=True)
    native_village = models.CharField(max_length=500, blank=True, null=True)
    district = models.CharField(max_length=500)
    tehsil = models.CharField(max_length=500, blank=True, null=True)
    current_address =  models.TextField()
    phone_number = models.CharField(unique=True, max_length=10)
    business_address = models.TextField(blank=True, null=True)
    business_phone_number = models.CharField(max_length=10, blank=True, null=True)
    marriage_profile_pic = models.ImageField(upload_to='marriage_profile_pics')

    # def age(self):
    #     today = date.today()
    #     age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    #     return age
        
    def save(self, *args, **kwargs):
        today = date.today()
        self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Marriage Profile'
        verbose_name_plural = 'Marriage Profiles'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CandidateProfile(DateFields):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='candidate_profiles', help_text='User who created this profile (can create multiple profiles for family members)')
    candidate_name = models.CharField(max_length=500)
    relationship_to_user = models.CharField(max_length=100, blank=True, null=True, help_text='Relationship to profile creator (e.g., Son, Daughter, Self, Brother, Sister, etc.)')
    is_shared = models.BooleanField(default=True, help_text='Share this profile in matrimonial listings') 
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    height = models.CharField(max_length=50)
    color = models.CharField(max_length=10, blank=True, null=True)
    education = models.CharField(max_length=500)
    occupation = models.CharField(max_length=500, blank=True, null=True)
    annual_income = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    time_of_birth = models.TimeField(blank=True, null=True)
    # blood_group = models.CharField(max_length=5, blank=True, null=True)
    is_manglik = models.BooleanField(default=False)
    gotra = models.CharField(max_length=100, blank=True, null=True)
    birth_place = models.CharField(max_length=500)
    father_or_guardian_occupation = models.CharField(max_length=500)
    city = models.CharField(max_length=500, null=True)
    current_address =  models.TextField()
    pincode = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    whatsapp_phone_number = models.CharField(max_length=10, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    partner_preference = models.CharField(max_length=500, blank=True, null=True)
    if_candidate_is_widow_widower_divorced_or_disabled = models.CharField(max_length=500, blank=True, null=True)
    marriage_profile_pic = models.ImageField(upload_to='marriage_profile_pics')

    # def age(self):
    #     today = date.today()
    #     age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    #     return age
        
    def save(self, *args, **kwargs):
        today = date.today()
        self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Marriage Profile'
        verbose_name_plural = 'Marriage Profiles'

    def __str__(self):
        return f'{self.candidate_name}'


class ShortlistedProfile(DateFields):
    """Model to track profiles shortlisted by users"""
    user = models.ForeignKey('administration.CustomUser', on_delete=models.CASCADE, related_name='shortlisted_profiles')
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='shortlisted_by')
    
    class Meta:
        verbose_name = 'Shortlisted Profile'
        verbose_name_plural = 'Shortlisted Profiles'
        unique_together = ('user', 'profile')  # Prevent duplicate shortlists
    
    def __str__(self):
        return f'{self.user.show_username()} shortlisted {self.profile.candidate_name}'
