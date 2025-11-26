from . import models
from django.contrib import admin

class CandidateProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'candidate_name', 'gender', 'color', 'height', 'education', 'occupation', 'annual_income', 'father_name', 'date_of_birth', 'time_of_birth', 'birth_place', 'gotra', 'city', 'current_address', 'phone_number', 'whatsapp_phone_number', 'marriage_profile_pic')
    # readonly_fields = ('user', 'candidate_name', 'gender', 'color', 'height', 'education', 'occupation', 'annual_income', 'father_name', 'date_of_birth', 'time_of_birth', 'birth_place', 'gotra', 'city', 'current_address', 'phone_number', 'whatsapp_phone_number', 'marriage_profile_pic')

admin.site.register(models.CandidateProfile, CandidateProfileAdmin)
# admin.site.register(models.MarriageProfile)
