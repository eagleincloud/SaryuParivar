# Python Imports
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local Imports
from . import models
from .forms import ProfileForm, CandidateProfileForm
from administration import models as admin_models

# def dashboard(request):
    # return render(request, 'dashboard.html', {'username': request.user.show_username(), 'user_avatar': request.user.profile_pic.url if hasattr(request.user, 'profile_pic') else None})


# def create_profile(request):
#     form = ProfileForm()
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             print('form saved')
#             messages.success(request, "Profile created successfully.")
#             return redirect('/dashboard/create_profile/')
#         else:
#             print(form.errors)
#             messages.error(request, form.errors)
#             # return render(request, 'create-profile.html', {'form':form})

#     return render(request, 'create-profile.html', {'form': form})


# def profile_create_edit(request):
#     try:
#         profile = models.MarriageProfile.objects.get(user=request.user)
#         form = ProfileForm(instance=profile)
#         profile_exists = True
#     except:
#         form = ProfileForm()
#         profile_exists = False

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile if profile_exists else None)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             messages.success(request, "Profile updated successfully.")
#             return redirect('/dashboard/my_profile/')
#         else:
#             messages.error(request, form.errors)

#     return render(request, 'profile-new.html', {'form': form, 'profile_exists': profile_exists, 'username': request.user.show_username(), 'user_avatar': request.user.profile_pic.url if hasattr(request.user, 'profile_pic') else None})


def profile_create_edit(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    try:
        profile = models.CandidateProfile.objects.get(user=request.user)
        form = CandidateProfileForm(instance=profile)
        profile_exists = True
    except:
        form = CandidateProfileForm()
        profile_exists = False

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile if profile_exists else None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('/dashboard/my_profile/')
        else:
            messages.error(request, form.errors)

    # Check payment status
    payment_pending = False
    pending_transaction = None
    if not request.user.payment_done:
        pending_transaction = admin_models.PaymentTransaction.objects.filter(
            user=request.user,
            payment_status='pending'
        ).first()
        if pending_transaction:
            payment_pending = True

    return render(request, 'profile-new.html', {
        'form': form, 
        'profile_exists': profile_exists, 
        'username': request.user.show_username(), 
        'user_avatar': request.user.profile_pic.url if hasattr(request.user, 'profile_pic') else '',
        'payment_pending': payment_pending,
        'pending_transaction': pending_transaction,
        'payment_done': request.user.payment_done,
    })


# def all_profiles(request):
#     page =1
#     # print(request.method)
#     # Handle POST method
#     if request.method == 'POST':
#         gender = request.POST.get('gender')
#         age_lower_limit = request.POST.get('age_lower_limit')
#         age_upper_limit = request.POST.get('age_upper_limit')
#         district = request.POST.get('district')
#         education = request.POST.get('education')

#         # print(gender, age_lower_limit, age_upper_limit, district, education)

#         # Filter profiles based on the POST data
#         profile_objs = models.MarriageProfile.objects.filter(
#             gender=gender,
#             age__gte=age_lower_limit,
#             age__lte=age_upper_limit,
#             district=district,
#             education=education
#         ).order_by('created_at')
#         print(profile_objs.count())
#         paginator = Paginator(profile_objs, 10)

#         try:
#             profiles_page = paginator.page(page)
#         except PageNotAnInteger:
#             profiles_page = paginator.page(1)
#         except EmptyPage:
#             profiles_page = paginator.page(paginator.num_pages)

#         profiles = [
#             {
#                 'id': profile.id,
#                 'first_name': profile.first_name,
#                 'last_name': profile.last_name,
#                 'father_name': profile.father_name,
#                 'education': profile.education,
#                 'height_feet': profile.height_feet,
#                 'height_inches': profile.height_inches,
#                 'color': profile.color,
#                 'age': profile.age,
#                 'native_village': profile.native_village,
#                 'gotra': profile.gotra,
#                 'gender': profile.gender,
#                 'marriage_profile_pic': profile.marriage_profile_pic.url if profile.marriage_profile_pic else None,
#             }
#             for profile in profiles_page.object_list
#         ]


#         return JsonResponse(
#             {
#                 'profiles': profiles,
#                 'page': profiles_page.number,
#                 'total_pages': paginator.num_pages,
#                 'total_profiles': paginator.count,
#                 'has_next': profiles_page.has_next(),
#                 'has_previous': profiles_page.has_previous(),
#             }
#         )
#     else:
#         if request.method == 'GET':
#             page = request.GET.get('page', 1)
    
#         user_avatar = request.user.profile_pic.url if hasattr(request.user, 'profile_pic') else None

#         # Get distinct values for filtering
#         genders = models.MarriageProfile.objects.values_list('gender', flat=True).distinct()
#         ages = models.MarriageProfile.objects.values_list('age', flat=True).distinct()
#         districts = models.MarriageProfile.objects.values_list('district', flat=True).distinct()
#         educations = models.MarriageProfile.objects.values_list('education', flat=True).distinct()
#         profile_objs = models.MarriageProfile.objects.all().order_by('created_at')
#         paginator = Paginator(profile_objs, 10)

#         try:
#             profiles = paginator.page(page)
#         except PageNotAnInteger:
#             profiles = paginator.page(1)
#         except EmptyPage:
#             profiles = paginator.page(paginator.num_pages)

#         context_data = {
#             'username': request.user.show_username(),
#             'user_avatar': user_avatar,
#             'genders': genders,
#             'ages': ages,
#             'districts': districts,
#             'educations': educations,
#             'profiles': profiles,
#             'page': profiles.number,
#             'total_pages': paginator.num_pages,
#             'total_profiles': paginator.count,
#             'has_next': profiles.has_next(),
#             'has_previous': profiles.has_previous(),
#         }

#         return render(request, 'all-profiles.html', context_data)


def all_profiles(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    
    # Note: We still return profiles even if payment not done, but they will be blurred
    # The payment_required flag is used to blur profiles in the frontend
    
    page =1
    # print(request.method)
    # Handle POST method
    if request.method == 'POST':
        # print(request.POST)
        page = int(request.POST.get('page_number', 1))
        # return JsonResponse({'hello':'hi'})
        gender = request.POST.get('gender')
        age_lower_limit = request.POST.get('age_lower_limit')
        age_upper_limit = request.POST.get('age_upper_limit')
        city = request.POST.get('city')
        education = request.POST.get('education')

        # print(bool(city), bool(education))
        # print(gender, age_lower_limit, age_lower_limit, city, education)
        # print(gender, age_lower_limit, age_upper_limit, district, education)
        # city=city,
        # education=education

        # Filter profiles based on the POST data
        # Exclude current user's own profile
        profile_objs = models.CandidateProfile.objects.filter(
            gender=gender,
            age__gte=age_lower_limit,
            age__lte=age_upper_limit,
        ).exclude(user=request.user)  # Exclude own profile
        if bool(city):
            profile_objs = profile_objs.filter(city=city)
        if bool(education):
            profile_objs = profile_objs.filter(education=education)
        profile_objs = profile_objs.order_by('created_at')
        print(profile_objs.count())
        paginator = Paginator(profile_objs, 4)

        # print(page)

        try:
            profiles_page = paginator.page(page)
        except PageNotAnInteger:
            profiles_page = paginator.page(1)
        except EmptyPage:
            # print('Empty page')
            profiles_page = paginator.page(paginator.num_pages)

        profiles = [
            {
                'id': profile.id if profile.id else '',
                'candidate_name': profile.candidate_name if profile.candidate_name else '',
                # 'last_name': profile.last_name,
                'father_name': profile.father_name if profile.father_name else '',
                'education': profile.education if profile.education else '',
                'height': profile.height if profile.height else '',
                # 'height_inches': profile.height_inches,
                'color': profile.color if profile.color else '',
                'date_of_birth': profile.date_of_birth if profile.date_of_birth else '',
                'time_of_birth': profile.time_of_birth if profile.time_of_birth else '',
                'birth_place': profile.birth_place if profile.birth_place else '',
                'current_address': profile.current_address if profile.current_address else '',
                'gotra': profile.gotra if profile.gotra else '',
                'gender': profile.gender if profile.gender else '',
                'phone_number': profile.phone_number if profile.phone_number else '',
                'occupation': profile.occupation if profile.occupation else '',
                'annual_income': profile.annual_income if profile.annual_income else '',
                'marriage_profile_pic': profile.marriage_profile_pic.url if profile.marriage_profile_pic else '',
            }
            for profile in profiles_page.object_list
            if profile.user != request.user  # Exclude own profile
        ]


        return JsonResponse(
            {
                'profiles': profiles,
                'page': profiles_page.number,
                'total_pages': tuple(range(1, paginator.num_pages+1)),
                'total_profiles': paginator.count,
                'has_next': profiles_page.has_next(),
                'has_previous': profiles_page.has_previous(),
                'payment_required': not request.user.payment_done,  # Add flag for frontend blur
            }
        )
    else:
        # Handle GET request
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
    
        user_avatar = request.user.profile_pic.url if hasattr(request.user, 'profile_pic') else ''

        # Get distinct values for filtering (filter out None/empty values)
        genders = [g for g in models.CandidateProfile.objects.values_list('gender', flat=True).distinct() if g]
        ages = [a for a in models.CandidateProfile.objects.values_list('age', flat=True).distinct() if a is not None]
        cities = [c for c in models.CandidateProfile.objects.values_list('city', flat=True).distinct() if c]
        educations = [e for e in models.CandidateProfile.objects.values_list('education', flat=True).distinct() if e]
        
        # Always load all profiles by default (will be blurred if user not verified)
        # Exclude current user's own profile
        profile_objs = models.CandidateProfile.objects.all().exclude(user=request.user).order_by('created_at')
        
        paginator = Paginator(profile_objs, 4)

        try:
            profiles = paginator.page(page)
        except PageNotAnInteger:
            profiles = paginator.page(1)
        except EmptyPage:
            profiles = paginator.page(paginator.num_pages)
        # print(page)

        context_data = {
            'username': request.user.show_username(),
            'user_avatar': user_avatar,
            'genders': genders,
            'ages': ages,
            'cities': cities,
            'educations': educations,
            'profiles': profiles,
            'page': profiles.number,
            'total_pages': tuple(range(1, paginator.num_pages+1)),
            'total_profiles': paginator.count,
            'has_next': profiles.has_next(),
            'has_previous': profiles.has_previous(),
        }
        # Payment status is added via context processor
        
        return render(request, 'all-profiles-new.html', context_data)
