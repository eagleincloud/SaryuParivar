# Python Imports
import string
import random
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Local Imports
from .mixins import FileDeleteMixin
from .utils import generate_otp_code

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


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    # head_of_the_family_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    father_name = models.CharField(max_length=200, null=True)
    # mother_name = models.CharField(max_length=200)
    # date_of_birth = models.DateField()
    # time_of_birth = models.TimeField(blank=True, null=True)
    # blood_group = models.CharField(max_length=5, blank=True, null=True)
    # gotra = models.CharField(max_length=100, blank=True, null=True)
    native_village = models.CharField(max_length=500, blank=True, null=True)
    district = models.CharField(max_length=500, null=True)
    tehsil = models.CharField(max_length=500, blank=True, null=True)
    current_address =  models.TextField(null=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    business_phone_number = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='user_profile_pics', null=True)
    payment_done = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.show_username()
    
    def show_username(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.username
    
    def generate_unique_username(self):
        username_base = f"{self.first_name.lower()}_{self.phone_number}"
        username = username_base
        
        while CustomUser.objects.filter(username=username).exists():
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{username_base}_{random_suffix}"

        return username
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_unique_username()
        super().save(*args, **kwargs)


class UserOTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_otp(user):
        """Generate OTP and send via SMS"""
        from .utils import generate_otp_code
        otp_code = generate_otp_code()  # Generate random 6-digit OTP
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        otp = UserOTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # Send OTP via SMS
        from .sms_service import SMSService
        phone_number = str(user.phone_number)
        success, message = SMSService.send_otp(phone_number, otp_code)
        
        if not success:
            print(f"⚠️ Failed to send OTP SMS: {message}")
            # Still return OTP object even if SMS fails (for testing)
            # In production, you might want to handle this differently
        
        return otp


class OTPRequestCounter(models.Model):
    """Track OTP requests to prevent abuse"""
    phone_number = models.CharField(max_length=10, unique=True)
    request_count = models.IntegerField(default=0)
    last_request_time = models.DateTimeField(null=True, blank=True)
    first_request_time = models.DateTimeField(auto_now_add=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'OTP Request Counter'
        verbose_name_plural = 'OTP Request Counters'
        ordering = ['-last_request_time']
    
    def __str__(self):
        return f"{self.phone_number} - {self.request_count} requests"
    
    def increment(self):
        """Increment request counter"""
        self.request_count += 1
        self.last_request_time = timezone.now()
        self.save()
    
    def reset(self):
        """Reset counter (called after time window)"""
        self.request_count = 0
        self.first_request_time = timezone.now()
        self.blocked_until = None
        self.save()
    
    def is_blocked(self):
        """Check if phone number is currently blocked"""
        if self.blocked_until:
            return timezone.now() < self.blocked_until
        return False
    
    def get_remaining_requests(self, max_requests=5):
        """Get remaining requests in current window"""
        return max(0, max_requests - self.request_count)
    
    def should_block(self, max_requests=5, time_window_minutes=60):
        """Check if should block based on rate limits"""
        if self.is_blocked():
            return True
        
        # Reset counter if time window has passed
        if self.last_request_time:
            time_diff = timezone.now() - self.first_request_time
            if time_diff.total_seconds() > time_window_minutes * 60:
                self.reset()
                return False
        
        # Block if exceeded max requests
        if self.request_count >= max_requests:
            # Block for remaining time in window
            if self.first_request_time:
                time_elapsed = (timezone.now() - self.first_request_time).total_seconds()
                time_remaining = (time_window_minutes * 60) - time_elapsed
                if time_remaining > 0:
                    self.blocked_until = timezone.now() + timezone.timedelta(seconds=time_remaining)
                    self.save()
            return True
        
        return False
    
    @staticmethod
    def get_or_create_counter(phone_number):
        """Get or create counter for phone number"""
        counter, created = OTPRequestCounter.objects.get_or_create(
            phone_number=phone_number,
            defaults={'request_count': 0}
        )
        return counter


class SamajGallery(DateFields):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='samaj_gallery')
    remarks = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Samaj Gallery'
        verbose_name_plural = 'Samaj Gallery'

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.title:
    #         self.title = f'Image {self.pk}'
    #     super().save(*args, **kwargs)


class SamajEvent(DateFields):
    title = models.CharField(max_length=100)
    date_of_event = models.DateField()
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Samaj Event'
        verbose_name_plural = 'Samaj Events'

    def __str__(self):
        return self.title
    

class Promotion(DateFields):
    banner = models.ImageField(upload_to='promotions')
    advertiser_name = models.CharField(max_length=500)
    advertiser_email = models.EmailField(blank=True, null=True)
    advertiser_phone = models.CharField(max_length=10, blank=True, null=True)
    expires_at = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Promotions'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        return self.advertiser_name


class Testimonial(DateFields):
    made_by = models.CharField(max_length=500)
    testimony = models.TextField()
    image = models.ImageField(upload_to='testimony_images')

    class Meta:
        verbose_name = 'Testimonials'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.made_by


class CommitteeMember(DateFields):
    """Model to store designated committee members of SaryuParin Brahmin Samaj"""
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, help_text='e.g., President, Secretary, Treasurer, etc.')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='committee_members', blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text='Show this member in the active committee')
    display_order = models.PositiveIntegerField(default=0, help_text='Order in which to display (lower numbers first)')

    class Meta:
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.designation}"


class PaymentTransaction(DateFields):
    """Model to track payment transactions"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='payment_transactions')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Verification'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    payment_proof = models.ImageField(upload_to='payment_proofs', null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    verified_at = models.DateTimeField(null=True, blank=True)
    admin_notified = models.BooleanField(default=False)
    admin_notified_at = models.DateTimeField(null=True, blank=True)
    # Annual subscription tracking
    subscription_start_date = models.DateField(null=True, blank=True, help_text='Date when subscription was activated')
    subscription_end_date = models.DateField(null=True, blank=True, help_text='Date when subscription expires (1 year from activation)')

    class Meta:
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.show_username()} - {self.payment_status} - {self.amount}"
    
    def notify_admin(self):
        """Mark that admin has been notified"""
        from django.utils import timezone
        self.admin_notified = True
        self.admin_notified_at = timezone.now()
        self.save()
    
    def is_pending_verification(self):
        """Check if payment is pending admin verification"""
        return self.payment_status == 'pending' and not self.verified_at
    
    def is_subscription_active(self):
        """Check if subscription is currently active"""
        if not self.subscription_end_date:
            return False
        from django.utils import timezone
        return timezone.now().date() <= self.subscription_end_date
    
    def is_subscription_expiring_soon(self, days=30):
        """Check if subscription is expiring within specified days"""
        if not self.subscription_end_date:
            return False
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        expiry_date = self.subscription_end_date
        days_until_expiry = (expiry_date - today).days
        return 0 <= days_until_expiry <= days
