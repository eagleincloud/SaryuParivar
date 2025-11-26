# Python Imports
from django.urls import path
from django.contrib.auth.decorators import login_required

# Local Imports
from . import views

urlpatterns = [
    path('', login_required(views.all_profiles), name='all_profiles'),
    # path('create_profile/', login_required(views.create_profile), name='create_profile'),
    path('my_profile/', login_required(views.profile_create_edit), name='profile')
    # path('all_profiles/', login_required(views.all_profiles), name='all_profiles')
]
