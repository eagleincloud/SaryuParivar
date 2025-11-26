# Python Imports
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

# Local Imports
from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_user, name='login_user'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('verify_firebase_otp/', views.verify_otp, name='verify_firebase_otp'),  # Firebase OTP verification
    path('logout/', login_required(views.logout_user), name='logout_user'),
    path('payment/', login_required(views.payment_page), name='payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('check_payment_status/', views.check_payment_status, name='check_payment_status'),
    
    # Password reset URLs
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             form_class=CustomPasswordResetForm,
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done')
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]
