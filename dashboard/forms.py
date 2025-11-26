from django import forms
from .models import MarriageProfile, CandidateProfile

# class CreateProfileForm(forms.ModelForm):
#     class Meta:
#         model = MarriageProfile
#         exclude = ['user',]

    # def clean(self):
    #     errors = []
    #     cleaned_data = super().clean()
    #     phone_number = cleaned_data.get("phone_number")
    #     business_phone_number = cleaned_data.get("business_phone_number")
        # if not phone_number or not str(phone_number).isdigit() or len(phone_number) != 10:
        #     errors.append('Invalid Phone: Phone number must be a 10 digit number')
        # if not str(business_phone_number).isdigit() or len(business_phone_number) != 10:
        #     errors.append('Invalid Business Phone: Business phone number must be a 10 digit number')
        # if len(errors) != 0:
            # raise forms.ValidationError(str(errors))
        
        # return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MarriageProfile
        exclude = ['user', 'age']
        widgets = {
            'head_of_the_family_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'family-head-name', 'placeholder': 'Name of the Head of the family'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'first-name', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'last-name', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'gender'}),
            'education': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'education', 'placeholder': 'Education'}),
            'father_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'father-name', 'placeholder': "Father's Name"}),
            'mother_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'mother-name', 'placeholder': "Mother's Name"}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date','class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'DOB', 'placeholder': 'Date of Birth'}),
            'time_of_birth': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'TOB', 'placeholder': 'Time of Birth'}),
            'blood_group': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'blood-group', 'placeholder': 'Blood Group'}),
            'gotra': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'gotra', 'placeholder': 'Gotra'}),
            'native_village': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'native-village', 'placeholder': 'Native Village'}),
            'district': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'dist', 'placeholder': 'Dist.'}),
            'tehsil': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'tehsil', 'placeholder': 'Tehsil'}),
            'current_address': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'current-address', 'placeholder': 'Current Address'}),
            'height_feet': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'height-feet', 'placeholder': 'Height Ft.', 'maxlength': '1'}),
            'height_inches': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'height-inches', 'placeholder': 'Height In.', 'maxlength': '2'}),
            'color': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'color', 'placeholder': 'Color'}),
            'phone_number': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'phone-number', 'placeholder': 'Phone Number'}),
            'business_address': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'business-address', 'placeholder': 'Business Address'}),
            'business_phone_number': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'business-phone-number', 'placeholder': 'Business Phone Number'}),
            'marriage_profile_pic': forms.ClearableFileInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0 custom-file-input', 'id': 'marriage-profile-pic'})
        }

    # def clean(self):
    #     errors = []
    #     cleaned_data = super().clean()
    #     phone_number = cleaned_data.get("phone_number")
    #     business_phone_number = cleaned_data.get("business_phone_number")
        # if not phone_number or not str(phone_number).isdigit() or len(phone_number) != 10:
        #     errors.append('Invalid Phone: Phone number must be a 10 digit number')
        # if not str(business_phone_number).isdigit() or len(business_phone_number) != 10:
        #     errors.append('Invalid Business Phone: Business phone number must be a 10 digit number')
        # if len(errors) != 0:
            # raise forms.ValidationError(str(errors))
        
        # return cleaned_data


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ['user', 'age']
        widgets = {
            # 'head_of_the_family_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'family-head-name', 'placeholder': 'Name of the Head of the family'}),
            'candidate_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'candidate-name', 'placeholder': "Candidate's name"}),
            # 'last_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'last-name', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'gender'}),
            'education': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'education', 'placeholder': 'Education'}),
            'occupation': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'occupation', 'placeholder': "Candidate's Occupation"}),
            'annual_income': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'annual-income', 'placeholder': "Annual Income"}),
            'father_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'father-name', 'placeholder': "Father's Name"}),
            'father_or_guardian_occupation': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'father-or-guardian-occupation', 'placeholder': "Father's/Guardian's Occupation"}),
            # 'mother_name': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'mother-name', 'placeholder': "Mother's Name"}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date','class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'DOB', 'placeholder': 'Date of Birth'}),
            'time_of_birth': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'TOB', 'placeholder': 'Time of Birth'}),
            # 'blood_group': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'blood-group', 'placeholder': 'Blood Group'}),
            'gotra': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'gotra', 'placeholder': 'Gotra'}),
            # 'current_address': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'current-address', 'placeholder': 'Current Address'}),
            # 'district': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'dist', 'placeholder': 'Dist.'}),
            # 'tehsil': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'tehsil', 'placeholder': 'Tehsil'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'city', 'placeholder': 'City'}),
            'current_address': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'current-address', 'placeholder': 'Current Address'}),
            'birth_place': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'birth-place', 'placeholder': 'Place of Birth'}),
            'height': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'height', 'placeholder': 'Height'}),
            # 'height_feet': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'height-feet', 'placeholder': 'Height Ft.', 'maxlength': '1'}),
            # 'height_inches': forms.NumberInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'height-inches', 'placeholder': 'Height In.', 'maxlength': '2'}),
            'color': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'color', 'placeholder': 'Color (Complexion)'}),
            'is_manglik': forms.CheckboxInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'is-manglik', 'placeholder': 'Is Manglik'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'phone-number', 'placeholder': 'Phone Number'}),
            # 'business_address': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'business-address', 'placeholder': 'Business Address'}),
            'whatsapp_phone_number': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'whatsapp-phone-number', 'placeholder': 'Whatsapp Phone Number'}),
            'email_id': forms.EmailInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'email-id', 'placeholder': 'Email'}),
            'pincode': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'pincode', 'placeholder': 'Pincode'}),
            'partner_preference': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'partner-preference', 'placeholder': 'Preference for Bride/Groom'}),
            'if_candidate_is_widow_widower_divorced_or_disabled': forms.TextInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0', 'id': 'if-candidate-is-widow-widower-divorced-or-disabled', 'placeholder': 'If the applicant is a Widower, Widow, Disabled, Divorced, please clearly write in the box'}),
            'marriage_profile_pic': forms.ClearableFileInput(attrs={'class': 'w-full p-1.5 bg-transparent border-b-[1px] border-[#000] poppins focus-visible:outline-0 custom-file-input', 'id': 'marriage-profile-pic'})
        }

    # def clean(self):
    #     errors = []
    #     cleaned_data = super().clean()
    #     phone_number = cleaned_data.get("phone_number")
    #     business_phone_number = cleaned_data.get("business_phone_number")
        # if not phone_number or not str(phone_number).isdigit() or len(phone_number) != 10:
        #     errors.append('Invalid Phone: Phone number must be a 10 digit number')
        # if not str(business_phone_number).isdigit() or len(business_phone_number) != 10:
        #     errors.append('Invalid Business Phone: Business phone number must be a 10 digit number')
        # if len(errors) != 0:
            # raise forms.ValidationError(str(errors))
        
        # return cleaned_data
