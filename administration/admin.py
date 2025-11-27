import datetime
from . import models
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


class UserAdmin(admin.ModelAdmin):
    fields =  ('first_name', 'last_name', 'native_village', 'district', 'tehsil', 'current_address', 'phone_number', 'business_address', 'business_phone_number', 'profile_pic','payment_done')
    # readonly_fields = ('created_at', 'updated_at')

class SamajEventForm(forms.ModelForm):
    class Meta:
        model = models.SamajEvent
        fields = '__all__'
        widgets = {
            'date_of_event': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean_date_of_event(self):
        date_of_event = self.cleaned_data.get('date_of_event')
        if isinstance(date_of_event, str):
            date_of_event = datetime.datetime.strptime(date_of_event, '%Y-%m-%dT%H:%M')
        return date_of_event

class SamajEventAdmin(admin.ModelAdmin):
    fields = ('title', 'date_of_event', 'remarks', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # form = SamajEventForm

    # def formatted_date_of_event(self, obj):
        # return obj.date_of_event.strftime('%I:%M %p')  # 12-hour format with AM/PM

    # formatted_date_of_event.short_description = 'Date of Event (12-hour format)'


class SamajGalleryAdmin(admin.ModelAdmin):
    fields = ('title', 'image', 'remarks', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'image', 'remarks')
    #     }),
    #     ('Timestamps', {
    #         'fields': ('created_at', 'updated_at'),
    #         'classes': ('collapse',),
    #     }),
    # )

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'payment_status_badge', 'has_proof', 'created_at', 'verified_at', 'pending_notification', 'quick_actions')
    list_filter = ('payment_status', 'created_at', 'admin_notified', 'verified_at')
    search_fields = ('transaction_id', 'user__phone_number', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'verified_at', 'admin_notified_at', 'payment_proof_preview')
    fields = ('user', 'transaction_id', 'amount', 'payment_status', 'payment_proof', 'payment_proof_preview', 'remarks', 'verified_by', 'verified_at', 'admin_notified', 'admin_notified_at', 'created_at', 'updated_at')
    actions = ['verify_payment', 'reject_payment']
    list_per_page = 25
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'completed': '#4caf50',
            'rejected': '#f44336',
            'failed': '#9e9e9e'
        }
        color = colors.get(obj.payment_status, '#9e9e9e')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Status'
    
    def payment_proof_preview(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" /></a>',
                obj.payment_proof.url, obj.payment_proof.url
            )
        return "No proof uploaded"
    payment_proof_preview.short_description = 'Payment Proof Preview'
    
    def quick_actions(self, obj):
        if obj.payment_status == 'pending':
            return format_html(
                '<div class="btn-group" role="group">'
                '<a href="/admin/administration/paymenttransaction/{}/change/?status=completed" class="btn btn-sm btn-success" style="margin-right: 5px; text-decoration: none;">✓ Verify</a>'
                '<a href="/admin/administration/paymenttransaction/{}/change/?status=rejected" class="btn btn-sm btn-danger" style="text-decoration: none;">✗ Reject</a>'
                '</div>',
                obj.id, obj.id
            )
        return "-"
    quick_actions.short_description = 'Quick Actions'
    
    def pending_notification(self, obj):
        """Show if admin needs to be notified"""
        if obj.payment_status == 'pending' and obj.payment_proof and not obj.admin_notified:
            return format_html(
                '<span style="background: #ff5722; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; animation: pulse 2s infinite;">'
                '⚠️ NEW - Needs Review'
                '</span>'
            )
        elif obj.payment_status == 'pending' and obj.payment_proof:
            return format_html(
                '<span style="background: #ff9800; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;">'
                '⏳ Pending Review'
                '</span>'
            )
        elif obj.payment_status == 'pending':
            return format_html(
                '<span style="background: #ffc107; color: #856404; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;">'
                '⏳ Awaiting Proof'
                '</span>'
            )
        return format_html(
            '<span style="background: #4caf50; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;">'
            '✅ Reviewed'
            '</span>'
        )
    pending_notification.short_description = 'Notification Status'
    
    def has_proof(self, obj):
        return bool(obj.payment_proof)
    has_proof.boolean = True
    has_proof.short_description = 'Has Proof'
    
    def verify_payment(self, request, queryset):
        """Admin action to verify payments"""
        from django.utils import timezone
        count = 0
        for transaction in queryset.filter(payment_status='pending'):
            transaction.payment_status = 'completed'
            transaction.verified_by = request.user
            transaction.verified_at = timezone.now()
            # Set annual subscription dates (1 year from verification)
            from datetime import timedelta
            transaction.subscription_start_date = timezone.now().date()
            transaction.subscription_end_date = transaction.subscription_start_date + timedelta(days=365)
            transaction.user.payment_done = True
            transaction.user.save()
            transaction.save()
            count += 1
        self.message_user(request, f'{count} payment(s) verified successfully.')
    verify_payment.short_description = 'Verify selected payments'
    
    def reject_payment(self, request, queryset):
        """Admin action to reject payments"""
        count = 0
        for transaction in queryset.filter(payment_status='pending'):
            transaction.payment_status = 'rejected'
            transaction.user.payment_done = False
            transaction.user.save()
            transaction.save()
            count += 1
        self.message_user(request, f'{count} payment(s) rejected.')
    reject_payment.short_description = 'Reject selected payments'
    
    def save_model(self, request, obj, form, change):
        from django.utils import timezone
        from django.contrib import messages
        
        # If admin is verifying payment
        if change:
            old_obj = models.PaymentTransaction.objects.get(pk=obj.pk) if obj.pk else None
            old_status = old_obj.payment_status if old_obj else None
            
            if obj.payment_status == 'completed' and old_status != 'completed':
                obj.verified_by = request.user
                obj.verified_at = timezone.now()
                # Set annual subscription dates (1 year from verification)
                from datetime import timedelta
                obj.subscription_start_date = timezone.now().date()
                obj.subscription_end_date = obj.subscription_start_date + timedelta(days=365)
                obj.user.payment_done = True
                obj.user.save()
                obj.save()
                messages.success(request, f'Payment verified successfully for {obj.user.show_username()}. Annual subscription activated until {obj.subscription_end_date.strftime("%B %d, %Y")}.')
            elif obj.payment_status == 'rejected' and old_status != 'rejected':
                obj.user.payment_done = False
                obj.user.save()
                messages.warning(request, f'Payment rejected for {obj.user.show_username()}. User access revoked.')
            elif obj.payment_status == 'pending' and obj.payment_proof and not obj.admin_notified:
                # Notify admin when payment proof is uploaded
                obj.notify_admin()
        else:
            # New payment transaction - notify admin if proof is uploaded
            if obj.payment_proof and not obj.admin_notified:
                obj.notify_admin()
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Show pending payments first, especially those with proof but not notified"""
        qs = super().get_queryset(request)
        # Order by: pending with proof first, then pending, then by date
        return qs.order_by(
            '-payment_status',
            '-admin_notified',  # Unnotified first
            '-created_at'
        )
    
    def changelist_view(self, request, extra_context=None):
        """Add notification count to admin list view"""
        extra_context = extra_context or {}
        
        # Count pending payments that need admin attention
        pending_with_proof = models.PaymentTransaction.objects.filter(
            payment_status='pending',
            payment_proof__isnull=False,
            admin_notified=False
        ).count()
        
        pending_total = models.PaymentTransaction.objects.filter(
            payment_status='pending'
        ).count()
        
        extra_context['pending_notifications'] = pending_with_proof
        extra_context['pending_total'] = pending_total
        
        return super().changelist_view(request, extra_context)

class OTPRequestCounterAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'request_count', 'last_request_time', 'is_blocked_status', 'blocked_until')
    list_filter = ('blocked_until', 'last_request_time')
    search_fields = ('phone_number',)
    readonly_fields = ('first_request_time', 'is_blocked_status')
    fields = ('phone_number', 'request_count', 'last_request_time', 'first_request_time', 'blocked_until', 'is_blocked_status')
    
    def is_blocked_status(self, obj):
        if obj.blocked_until:
            from django.utils import timezone
            return timezone.now() < obj.blocked_until
        return False
    is_blocked_status.boolean = True
    is_blocked_status.short_description = 'Currently Blocked'

# Customize admin site header
admin.site.site_header = "Saryu Parivar Admin Panel"
admin.site.site_title = "Saryu Parivar Admin"
admin.site.index_title = "Welcome to Saryu Parivar Administration"

# Add pending payments count to admin
def get_pending_payments_count():
    return models.PaymentTransaction.objects.filter(payment_status='pending', payment_proof__isnull=False).count()

# Override admin index to show pending payments with notification
from django.contrib.admin import AdminSite
from django.utils.html import format_html
original_index = admin.site.index

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}
    pending_count = get_pending_payments_count()
    extra_context['pending_payments_count'] = pending_count
    
    # Add notification badge
    if pending_count > 0:
        extra_context['pending_payments_notification'] = format_html(
            '<div class="alert alert-warning" style="margin: 20px; border-left: 5px solid #ff9800; background: linear-gradient(135deg, #fff8e1 0%, #ffe082 100%); border-radius: 12px; padding: 20px; box-shadow: 0 8px 24px rgba(255, 152, 0, 0.25);">'
            '<div class="d-flex align-items-center">'
            '<div style="width: 48px; height: 48px; background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 16px; box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);">'
            '<i class="bx bx-bell" style="font-size: 28px; color: white;"></i>'
            '</div>'
            '<div class="flex-grow-1">'
            '<h4 style="color: #e65100; font-weight: 700; margin-bottom: 8px;">⚠️ Payment Verification Required</h4>'
            '<p style="color: #bf360c; margin-bottom: 12px;">You have <strong style="font-size: 20px; color: #ff9800;">{}</strong> pending payment(s) waiting for verification.</p>'
            '<a href="/admin/administration/paymenttransaction/?payment_status__exact=pending" class="btn btn-sm" style="background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; font-weight: 600; text-decoration: none; box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);">'
            '<i class="bx bx-credit-card"></i> Review Pending Payments'
            '</a>'
            '</div>'
            '</div>'
            '</div>',
            pending_count
        )
    
    return original_index(request, extra_context)

admin.site.index = custom_index

class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'phone_number', 'email', 'is_active', 'display_order')
    list_filter = ('is_active', 'designation')
    search_fields = ('name', 'designation', 'phone_number', 'email')
    fields = ('name', 'designation', 'phone_number', 'email', 'address', 'photo', 'is_active', 'display_order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('display_order', 'is_active')

admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.SamajGallery, SamajGalleryAdmin)
admin.site.register(models.SamajEvent, SamajEventAdmin)
admin.site.register(models.PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(models.OTPRequestCounter, OTPRequestCounterAdmin)
admin.site.register(models.CommitteeMember, CommitteeMemberAdmin)
# admin.site.register(models.UserOTP)
admin.site.register(models.Promotion)
admin.site.register(models.Testimonial)
# admin.site.register(UserOTP)