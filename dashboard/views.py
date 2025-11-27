# Python Imports
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local Imports
from . import models
from .forms import ProfileForm, CandidateProfileForm, UserProfileForm
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


def user_profile(request):
    """Edit user's own profile information - RENDERS user-profile.html"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        user = request.user
        form = UserProfileForm(instance=user)
        
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile information has been updated successfully.")
                return redirect('/dashboard/user_profile/')
            else:
                messages.error(request, form.errors)
        
        user_avatar = ''
        if hasattr(user, 'profile_pic') and user.profile_pic:
            try:
                user_avatar = user.profile_pic.url
            except Exception as e:
                user_avatar = ''
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Error accessing user avatar: {e}")
        
        return render(request, 'user-profile.html', {
            'form': form,
            'user': user,
            'username': user.show_username(),
            'user_avatar': user_avatar,
            'payment_done': user.payment_done,
        })
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        error_msg = f"Error in user_profile view: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        try:
            messages.error(request, f"An error occurred while loading your profile: {str(e)}")
        except:
            pass
        try:
            user = request.user if request.user.is_authenticated else None
            if user:
                form = UserProfileForm(instance=user)
                username = user.show_username() if hasattr(user, 'show_username') else str(user)
                payment_done = getattr(user, 'payment_done', False)
            else:
                form = UserProfileForm()
                username = ''
                payment_done = False
            return render(request, 'user-profile.html', {
                'form': form,
                'user': user,
                'username': username,
                'user_avatar': '',
                'payment_done': payment_done,
            })
        except Exception as render_error:
            logger.error(f"Could not render user-profile.html even with fallback: {render_error}")
            return redirect('/dashboard/')


def my_profiles(request):
    """List all matrimonial profiles created by the user"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        profiles = models.CandidateProfile.objects.filter(user=request.user).order_by('-created_at')
        
        # Add safe image URL access to each profile
        for profile in profiles:
            profile.safe_image_url = ''
            if profile.marriage_profile_pic:
                try:
                    profile.safe_image_url = profile.marriage_profile_pic.url
                except Exception as e:
                    profile.safe_image_url = ''
                    # Log error but don't break the page
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error accessing image for profile {profile.id}: {e}")
        
        user_avatar = ''
        if hasattr(request.user, 'profile_pic') and request.user.profile_pic:
            try:
                user_avatar = request.user.profile_pic.url
            except Exception as e:
                user_avatar = ''
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Error accessing user avatar: {e}")
        
        return render(request, 'my-profiles.html', {
            'profiles': profiles,
            'username': request.user.show_username(),
            'user_avatar': user_avatar,
            'payment_done': request.user.payment_done,
        })
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error in my_profiles view: {e}\n{traceback.format_exc()}")
        messages.error(request, f"An error occurred while loading your profiles: {str(e)}")
        return redirect('/dashboard/')


def shortlisted_profiles(request):
    """List all shortlisted profiles by the user - RENDERS shortlisted-profiles.html"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        shortlisted = models.ShortlistedProfile.objects.filter(user=request.user).select_related('profile').order_by('-created_at')
        profiles = [sp.profile for sp in shortlisted]
        
        # Add safe image URL access to each profile
        for profile in profiles:
            profile.safe_image_url = ''
            if profile.marriage_profile_pic:
                try:
                    profile.safe_image_url = profile.marriage_profile_pic.url
                except Exception as e:
                    profile.safe_image_url = ''
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error accessing image for profile {profile.id}: {e}")
        
        user_avatar = ''
        if hasattr(request.user, 'profile_pic') and request.user.profile_pic:
            try:
                user_avatar = request.user.profile_pic.url
            except Exception as e:
                user_avatar = ''
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Error accessing user avatar: {e}")
        
        return render(request, 'shortlisted-profiles.html', {
            'profiles': profiles,
            'username': request.user.show_username(),
            'user_avatar': user_avatar,
            'payment_done': request.user.payment_done,
        })
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        error_msg = f"Error in shortlisted_profiles view: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        try:
            messages.error(request, f"An error occurred while loading your shortlisted profiles: {str(e)}")
        except:
            pass
        try:
            user = request.user if request.user.is_authenticated else None
            username = user.show_username() if user and hasattr(user, 'show_username') else ''
            payment_done = getattr(user, 'payment_done', False) if user else False
            return render(request, 'shortlisted-profiles.html', {
                'profiles': [],
                'username': username,
                'user_avatar': '',
                'payment_done': payment_done,
            })
        except Exception as render_error:
            logger.error(f"Could not render shortlisted-profiles.html even with empty data: {render_error}")
            return redirect('/dashboard/')


def toggle_shortlist(request, profile_id):
    """Toggle shortlist status of a profile"""
    if request.user.is_superuser:
        return JsonResponse({'error': 'Admin users cannot shortlist profiles'}, status=403)
    
    try:
        profile = models.CandidateProfile.objects.get(id=profile_id, is_shared=True)
        
        # Check if already shortlisted
        shortlisted, created = models.ShortlistedProfile.objects.get_or_create(
            user=request.user,
            profile=profile
        )
        
        if not created:
            # Already shortlisted, remove it
            shortlisted.delete()
            is_shortlisted = False
            message = f"Removed {profile.candidate_name} from shortlist"
        else:
            # Added to shortlist
            is_shortlisted = True
            message = f"Added {profile.candidate_name} to shortlist"
        
        return JsonResponse({
            'success': True,
            'is_shortlisted': is_shortlisted,
            'message': message
        })
    except models.CandidateProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def profile_create_edit(request, profile_id=None):
    """Create or edit a profile for family member"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    profile = None
    profile_exists = False
    
    if profile_id:
        try:
            profile = models.CandidateProfile.objects.get(id=profile_id, user=request.user)
            profile_exists = True
        except models.CandidateProfile.DoesNotExist:
            messages.error(request, "Profile not found.")
            return redirect('/dashboard/my_profiles/')
    
    form = CandidateProfileForm(instance=profile) if profile else CandidateProfileForm()

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # Set is_shared to True by default (can be toggled later)
            if not profile.id:  # New profile
                profile.is_shared = True
            profile.save()
            messages.success(request, f"Profile for {profile.candidate_name} saved successfully.")
            return redirect('/dashboard/my_profiles/')
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

    user_avatar = ''
    if hasattr(request.user, 'profile_pic') and request.user.profile_pic:
        try:
            user_avatar = request.user.profile_pic.url
        except:
            user_avatar = ''
    
    return render(request, 'profile-new.html', {
        'form': form, 
        'profile_exists': profile_exists,
        'profile': profile,
        'username': request.user.show_username(), 
        'user_avatar': user_avatar,
        'payment_pending': payment_pending,
        'pending_transaction': pending_transaction,
        'payment_done': request.user.payment_done,
    })


def toggle_profile_share(request, profile_id):
    """Toggle profile sharing status"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        profile = models.CandidateProfile.objects.get(id=profile_id, user=request.user)
        profile.is_shared = not profile.is_shared
        profile.save()
        status = "shared" if profile.is_shared else "unshared"
        messages.success(request, f"Profile for {profile.candidate_name} is now {status}.")
    except models.CandidateProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
    
    return redirect('/dashboard/my_profiles/')


def delete_profile(request, profile_id):
    """Delete a profile"""
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        profile = models.CandidateProfile.objects.get(id=profile_id, user=request.user)
        candidate_name = profile.candidate_name
        profile.delete()
        messages.success(request, f"Profile for {candidate_name} deleted successfully.")
    except models.CandidateProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
    
    return redirect('/dashboard/my_profiles/')


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
        # Only show shared profiles, exclude current user's own profiles
        profile_objs = models.CandidateProfile.objects.filter(is_shared=True).exclude(user=request.user)
        
        # Apply filters only if values are provided
        if gender:
            profile_objs = profile_objs.filter(gender=gender)
        if age_lower_limit:
            profile_objs = profile_objs.filter(age__gte=int(age_lower_limit))
        if age_upper_limit:
            profile_objs = profile_objs.filter(age__lte=int(age_upper_limit))
        if city:
            profile_objs = profile_objs.filter(city=city)
        if education:
            profile_objs = profile_objs.filter(education=education)
        profile_objs = profile_objs.order_by('created_at')
        paginator = Paginator(profile_objs, 4)

        # print(page)

        try:
            profiles_page = paginator.page(page)
        except PageNotAnInteger:
            profiles_page = paginator.page(1)
        except EmptyPage:
            # print('Empty page')
            profiles_page = paginator.page(paginator.num_pages)

        # Get shortlisted profile IDs for current user
        shortlisted_ids = set(
            models.ShortlistedProfile.objects.filter(user=request.user)
            .values_list('profile_id', flat=True)
        )

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
                'date_of_birth': str(profile.date_of_birth) if profile.date_of_birth else '',
                'time_of_birth': str(profile.time_of_birth) if profile.time_of_birth else '',
                'birth_place': profile.birth_place if profile.birth_place else '',
                'current_address': profile.current_address if profile.current_address else '',
                'gotra': profile.gotra if profile.gotra else '',
                'gender': profile.gender if profile.gender else '',
                'phone_number': profile.phone_number if profile.phone_number else '',
                'whatsapp_phone_number': profile.whatsapp_phone_number if profile.whatsapp_phone_number else '',
                'email_id': profile.email_id if profile.email_id else '',
                'occupation': profile.occupation if profile.occupation else '',
                'annual_income': profile.annual_income if profile.annual_income else '',
                'marriage_profile_pic': profile.marriage_profile_pic.url if profile.marriage_profile_pic else '',
                'is_shortlisted': profile.id in shortlisted_ids,
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
    
        user_avatar = ''
        if hasattr(request.user, 'profile_pic') and request.user.profile_pic:
            try:
                user_avatar = request.user.profile_pic.url
            except:
                user_avatar = ''

        # Get distinct values for filtering (filter out None/empty values)
        genders = [g for g in models.CandidateProfile.objects.values_list('gender', flat=True).distinct() if g]
        ages = [a for a in models.CandidateProfile.objects.values_list('age', flat=True).distinct() if a is not None]
        cities = [c for c in models.CandidateProfile.objects.values_list('city', flat=True).distinct() if c]
        educations = [e for e in models.CandidateProfile.objects.values_list('education', flat=True).distinct() if e]
        
        # Always load all shared profiles by default (will be blurred if user not verified)
        # Exclude current user's own profiles
        profile_objs = models.CandidateProfile.objects.filter(is_shared=True).exclude(user=request.user).order_by('created_at')
        
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
