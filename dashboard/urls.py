# Python Imports
from django.urls import path
from django.contrib.auth.decorators import login_required

# Local Imports
from . import views

urlpatterns = [
    path('', login_required(views.all_profiles), name='all_profiles'),
    path('user_profile/', login_required(views.user_profile), name='user_profile'),
    path('my_profiles/', login_required(views.my_profiles), name='my_profiles'),
    path('shortlisted_profiles/', login_required(views.shortlisted_profiles), name='shortlisted_profiles'),
    path('create_profile/', login_required(views.profile_create_edit), name='create_profile'),
    path('edit_profile/<int:profile_id>/', login_required(views.profile_create_edit), name='edit_profile'),
    path('toggle_share/<int:profile_id>/', login_required(views.toggle_profile_share), name='toggle_profile_share'),
    path('toggle_shortlist/<int:profile_id>/', login_required(views.toggle_shortlist), name='toggle_shortlist'),
    path('delete_profile/<int:profile_id>/', login_required(views.delete_profile), name='delete_profile'),
    path('my_profile/', login_required(views.user_profile), name='profile'),  # Redirect old URL to user profile
]
