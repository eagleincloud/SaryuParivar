# Python Imports
import json
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Local Imports
from . import models
from .forms import RegistrationForm, CustomPasswordResetForm

def homepage(request):
    # Check if this is a registration POST - handle it before checking authentication
    # This ensures registration redirect works even if user becomes authenticated during registration
    if request.method == 'POST':
        # Check if it's a registration form (has registration fields)
        if 'first_name' in request.POST or 'phone_number' in request.POST or request.POST.get('form_type') == 'Registration':
            return registration_page(request)
    
    # Only redirect authenticated users on GET requests
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    else:
        samaj_gallery_images = models.SamajGallery.objects.all()
        promotions = models.Promotion.objects.filter(
            Q(expires_at__gte=now().date()) | Q(expires_at__isnull=True)
        )
        testimonials = models.Testimonial.objects.all().order_by('-updated_at')[:4]
        # print(promotions.count())
        samaj_event_objs = models.SamajEvent.objects.all().order_by('-date_of_event')[:4]
        samaj_events = [
            {
                'title': samaj_event.title,
                'date_of_event': samaj_event.date_of_event.strftime('%d %b, %Y')
            } for samaj_event in samaj_event_objs
        ]
        # Get active committee members
        committee_members = models.CommitteeMember.objects.filter(is_active=True).order_by('display_order', 'name')
        
        # Check if this is a redirect after registration (ONLY show modal if URL parameter exists)
        registration_success = request.GET.get('registration_success') == '1'
        txn_id_from_url = request.GET.get('txn_id')  # Fallback: transaction ID from URL
        
        # Get pending payment info from session ONLY if registration_success is True
        # This prevents modal from showing on every page load
        pending_payment_user_id = None
        pending_payment_transaction_id = None
        payment_transaction = None
        payment_amount = 500.00  # Default amount
        
        if registration_success:
            # Only get session data if this is a redirect after registration
            pending_payment_user_id = request.session.get('pending_payment_user_id')
            pending_payment_transaction_id = request.session.get('pending_payment_transaction_id')
            
            print(f"🔍 Registration success detected - User ID: {pending_payment_user_id}, Transaction ID: {pending_payment_transaction_id}")
            print(f"🔍 Transaction ID from URL: {txn_id_from_url}")
            
            # Try to get transaction from session ID first
            if pending_payment_transaction_id:
                try:
                    payment_transaction = models.PaymentTransaction.objects.get(id=pending_payment_transaction_id)
                    payment_amount = float(payment_transaction.amount)
                    print(f"✅ Payment transaction found: {payment_transaction.transaction_id}, Amount: ₹{payment_amount}")
                except models.PaymentTransaction.DoesNotExist:
                    print(f"⚠️  Payment transaction not found for ID: {pending_payment_transaction_id}")
                    pending_payment_transaction_id = None
            
            # Fallback: Try to get transaction from URL parameter
            if not payment_transaction and txn_id_from_url:
                try:
                    payment_transaction = models.PaymentTransaction.objects.filter(transaction_id=txn_id_from_url).first()
                    if payment_transaction:
                        pending_payment_transaction_id = payment_transaction.id
                        payment_amount = float(payment_transaction.amount)
                        print(f"✅ Payment transaction found from URL: {payment_transaction.transaction_id}, Amount: ₹{payment_amount}")
                except Exception as e:
                    print(f"⚠️  Error getting transaction from URL: {e}")
            
            # If still no transaction, try to get from user
            if not payment_transaction and pending_payment_user_id:
                try:
                    user = models.CustomUser.objects.get(id=pending_payment_user_id)
                    payment_transaction = models.PaymentTransaction.objects.filter(user=user, payment_status='pending').first()
                    if payment_transaction:
                        pending_payment_transaction_id = payment_transaction.id
                        payment_amount = float(payment_transaction.amount)
                        print(f"✅ Payment transaction found from user: {payment_transaction.transaction_id}, Amount: ₹{payment_amount}")
                except Exception as e:
                    print(f"⚠️  Error getting transaction from user: {e}")
            
            if not payment_transaction:
                print(f"⚠️  No payment transaction found - clearing session data")
                # Clear invalid session data
                if 'pending_payment_user_id' in request.session:
                    del request.session['pending_payment_user_id']
                if 'pending_payment_transaction_id' in request.session:
                    del request.session['pending_payment_transaction_id']
                pending_payment_user_id = None
                pending_payment_transaction_id = None
        else:
            # If no registration_success parameter, clear any stale session data
            # This prevents modal from showing on normal page visits
            if 'pending_payment_user_id' in request.session:
                del request.session['pending_payment_user_id']
            if 'pending_payment_transaction_id' in request.session:
                del request.session['pending_payment_transaction_id']
        
        context = {
            'samaj_gallery_images': samaj_gallery_images,
            'samaj_events': samaj_events,
            'promotions': promotions,
            'testimonials': testimonials,
            'committee_members': committee_members,
            'registration_success': registration_success,
            # Always provide payment variables to prevent template errors
            'payment_amount': None,
            'pending_payment_user_id': None,
            'pending_payment_transaction_id': None,
            'payment_transaction': None,
        }
        
        # Add payment info to context if registration_success is True
        if registration_success:
            context['registration_success'] = True
            context['payment_amount'] = payment_amount
            if pending_payment_user_id:
                context['pending_payment_user_id'] = pending_payment_user_id
            if pending_payment_transaction_id:
                context['pending_payment_transaction_id'] = pending_payment_transaction_id
            if payment_transaction:
                context['payment_transaction'] = payment_transaction
            print(f"✅ Context prepared - registration_success: True, txn_id: {pending_payment_transaction_id}, amount: ₹{payment_amount}")
        
        return render(request, 'index.html', context)


def registration_page(request):
    # Don't redirect authenticated users if this is a POST (they might be registering)
    # Only redirect if it's a GET request from an authenticated user
    if request.method == 'GET' and request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    
    # Handle POST requests (registration form submission)
    if request.method == 'POST':
        print(f"📝 Registration POST received - User authenticated: {request.user.is_authenticated}")
        try:
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.payment_done = False  # Payment not done initially
                # Password is already set in form.save() via set_password
                user.save()
                print('form saved')
                # Create pending payment transaction
                import uuid
                transaction_id = f"TXN{user.phone_number}{uuid.uuid4().hex[:8].upper()}"
                payment_transaction = models.PaymentTransaction.objects.create(
                    user=user,
                    transaction_id=transaction_id,
                    amount=500.00,  # Set your registration fee amount
                    payment_status='pending'
                )
                # Store payment transaction ID in session BEFORE login
                request.session['pending_payment_transaction_id'] = payment_transaction.id
                request.session['registration_success'] = True
                request.session.modified = True
                request.session.save()
                
                # Auto-login the user after registration
                login(request, user)
                print(f"✅ User auto-logged in: {user.show_username()}")
                
                # Show success message
                messages.success(request, f"Account created successfully! Welcome {user.show_username()}. Please complete the payment to access the portal.")
                
                # Ensure session is saved after login
                request.session.save()
                
                print(f"✅ Registration successful - User: {user.show_username()}, Transaction: {payment_transaction.transaction_id}")
                print(f"✅ Redirecting to payment page: /payment/")
                
                # Redirect directly to payment page with success message
                # Use HttpResponseRedirect to ensure redirect happens
                from django.http import HttpResponseRedirect
                payment_url = '/payment/?registration_success=1'
                print(f"🔄 Redirecting to: {payment_url}")
                
                # Create redirect response
                response = HttpResponseRedirect(payment_url)
                print(f"✅ Redirect response created: {response.status_code}")
                return response
            else:
                print(f"❌ Form validation errors: {form.errors}")
                print(f"❌ Form data received: {list(request.POST.keys())}")
                print(f"❌ Files received: {list(request.FILES.keys()) if request.FILES else 'None'}")
                print(f"❌ POST data values: {dict(request.POST)}")
                
                # Format errors for better display
                error_messages = []
                for field, errors in form.errors.items():
                    # Make field names more user-friendly
                    field_name = field.replace('_', ' ').title()
                    for error in errors:
                        if field == '__all__':
                            error_messages.append(str(error))
                        else:
                            error_messages.append(f"{field_name}: {str(error)}")
                
                error_msg = "Please correct the following errors: " + " | ".join(error_messages)
                print(f"❌ Error message: {error_msg}")
                messages.error(request, error_msg)
                # Return to homepage with error message (will show in modal)
                return redirect('/?registration_error=1')
        except Exception as e:
            print(f"❌ Registration error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Get a user-friendly error message
            error_msg = str(e)
            if 'phone_number' in error_msg.lower() or 'unique' in error_msg.lower():
                error_msg = "This phone number is already registered. Please use a different phone number or try logging in."
            elif 'image' in error_msg.lower() or 'pillow' in error_msg.lower():
                error_msg = "Error processing image. Please upload a valid image file (JPG, PNG) under 5MB."
            else:
                error_msg = f"Registration failed: {error_msg}. Please check all fields and try again."
            
            messages.error(request, error_msg)
            return redirect('/?registration_error=1')
    
    # If GET request and not authenticated, redirect to homepage
    # (This should not happen as homepage handles GET requests)
    return redirect('/')


def login_user(request):
    """Login view using username/phone/email + password"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    
    if request.method == 'POST':
        try:
            username_or_phone_or_email = request.POST.get('username_or_phone', '').strip()
            password = request.POST.get('password', '')
            
            if not username_or_phone_or_email or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Please provide both username/phone/email and password'
                }, status=400)
            
            # Try to find user by username, phone number, or email
            user = None
            try:
                # Try username first
                user = models.CustomUser.objects.get(username=username_or_phone_or_email, is_active=True)
            except models.CustomUser.DoesNotExist:
                try:
                    # Try phone number
                    user = models.CustomUser.objects.get(phone_number=username_or_phone_or_email, is_active=True)
                except models.CustomUser.DoesNotExist:
                    try:
                        # Try email (case-insensitive) - only if email is not empty
                        if username_or_phone_or_email and '@' in username_or_phone_or_email:
                            user = models.CustomUser.objects.filter(
                                email__iexact=username_or_phone_or_email, 
                                is_active=True
                            ).first()
                    except Exception as e:
                        print(f"Error looking up user by email: {e}")
                        pass
            
            if user:
                # Authenticate with password
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    
                    # Check payment status
                    payment_pending = False
                    pending_transaction = models.PaymentTransaction.objects.filter(
                        user=user,
                        payment_status='pending'
                    ).first()
                    if pending_transaction:
                        payment_pending = True
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful!' + (' Your payment verification is pending.' if payment_pending else ''),
                        'redirect': '/dashboard/',
                        'payment_pending': payment_pending,
                        'payment_done': user.payment_done
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid password. Please try again.'
                    }, status=401)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found. Please check your username/phone/email or register first.'
                }, status=404)
        except Exception as e:
            import traceback
            print(f"Login error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': f'An error occurred during login: {str(e)}. Please try again.'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def send_otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        recaptcha_token = data.get('recaptcha_token')  # Firebase reCAPTCHA token
        
        # Check rate limiting
        counter = models.OTPRequestCounter.get_or_create_counter(phone_number)
        
        # Check if blocked
        if counter.is_blocked():
            blocked_until = counter.blocked_until
            if blocked_until:
                from django.utils import timezone
                seconds_remaining = (blocked_until - timezone.now()).total_seconds()
                return JsonResponse({
                    'success': False,
                    'message': f'Too many requests. Please try again in {int(seconds_remaining)} seconds.',
                    'blocked': True,
                    'seconds_remaining': int(seconds_remaining),
                    'request_count': counter.request_count
                }, status=429)
        
        # Check if should block
        if counter.should_block(max_requests=5, time_window_minutes=60):
            blocked_until = counter.blocked_until
            if blocked_until:
                from django.utils import timezone
                seconds_remaining = (blocked_until - timezone.now()).total_seconds()
                return JsonResponse({
                    'success': False,
                    'message': f'Rate limit exceeded. Please try again in {int(seconds_remaining)} seconds.',
                    'blocked': True,
                    'seconds_remaining': int(seconds_remaining),
                    'request_count': counter.request_count
                }, status=429)
        
        user = models.CustomUser.objects.filter(phone_number=phone_number)
        if user.exists():
            user = user.first()
            
            # Increment counter
            counter.increment()
            
            # Get remaining requests
            remaining = counter.get_remaining_requests(max_requests=5)
            
            # Generate and send OTP via backend SMS service
            try:
                otp_obj = models.UserOTP.generate_otp(user)
                return JsonResponse({
                    'success': True, 
                    'message': f'OTP sent successfully to {phone_number}. Please check your phone.',
                    'phone_number': phone_number,
                    'request_count': counter.request_count,
                    'remaining_requests': remaining,
                    'max_requests': 5,
                    'otp_method': 'sms'  # Indicate backend SMS method
                }, status=200)
            except Exception as e:
                print(f"Error generating/sending OTP: {e}")
                return JsonResponse({
                    'success': False,
                    'message': f'Failed to send OTP: {str(e)}. Please try again.',
                    'phone_number': phone_number
                }, status=500)
        else:
            return JsonResponse({'success': False, 'message':'User not found'}, status=404)
    return redirect('/')


def verify_otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/dashboard/')
    
    if request.method == 'POST':
        # Check if it's Firebase authentication (JSON) or traditional OTP (form data)
        if request.content_type == 'application/json':
            # Firebase authentication
            data = json.loads(request.body)
            id_token = data.get('id_token')
            phone_number = data.get('phone_number')
            
            if not id_token or not phone_number:
                return JsonResponse({'success': False, 'message': 'Missing id_token or phone_number'}, status=400)
            
            # Verify Firebase ID token
            from .firebase_auth import verify_firebase_id_token
            firebase_user = verify_firebase_id_token(id_token)
            
            if firebase_user:
                # Get phone number from Firebase user
                firebase_phone = firebase_user.get('phone_number', '')
                # Remove country code if present
                if firebase_phone.startswith('+91'):
                    firebase_phone = firebase_phone[3:]
                elif firebase_phone.startswith('91'):
                    firebase_phone = firebase_phone[2:]
                
                # Get user from database using the phone number from Firebase or provided phone number
                user = models.CustomUser.objects.filter(phone_number=firebase_phone or phone_number).first()
                if user:
                    # Verify phone number matches (either from Firebase or provided)
                    if firebase_phone == phone_number or not firebase_phone:
                        # Allow login even if payment is pending - they'll see the banner
                        # Check payment status
                        payment_pending = False
                        pending_transaction = models.PaymentTransaction.objects.filter(
                            user=user,
                            payment_status='pending'
                        ).first()
                        if pending_transaction:
                            payment_pending = True
                        login(request, user)
                        return JsonResponse({
                            'success': True,
                            'message': 'Login successful. ' + ('Your payment verification is pending.' if payment_pending else ''),
                            'redirect': '/dashboard/',
                            'payment_pending': payment_pending,
                            'payment_done': user.payment_done
                        }, status=200)
                    else:
                        return JsonResponse({'success': False, 'message': 'Phone number mismatch'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid Firebase token'}, status=400)
        else:
            # Backend SMS OTP verification
            phone_number = request.POST.get('otp_phone_number')
            otp = request.POST.get('otp')
            
            if not phone_number or not otp:
                return JsonResponse({'success': False, 'message': 'Phone number and OTP are required'}, status=400)
            
            user = models.CustomUser.objects.filter(phone_number=phone_number).first()
            if user:
                user_otp_obj = models.UserOTP.objects.filter(
                    user=user,
                    otp_code=otp
                ).order_by('-created_at').first()
                
                if user_otp_obj and not user_otp_obj.is_expired():
                    # Valid OTP - login user
                    login(request, user)
                    user_otp_obj.delete()
                    
                    # Check payment status
                    payment_pending = False
                    pending_transaction = models.PaymentTransaction.objects.filter(
                        user=user,
                        payment_status='pending'
                    ).first()
                    if pending_transaction:
                        payment_pending = True
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful!' + (' Your payment verification is pending.' if payment_pending else ''),
                        'redirect': '/dashboard/',
                        'payment_pending': payment_pending,
                        'payment_done': user.payment_done
                    }, status=200)
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid or expired OTP. Please request a new OTP.'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/')


def payment_page(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the payment page.')
        return redirect('/?next=/payment/')
    
    if request.user.is_superuser:
        return redirect('/admin/')
    
    username = request.user.show_username()
    user_avatar = request.user.profile_pic.url if hasattr(request.user, 'profile_pic') and request.user.profile_pic else ''
    
    # Get payment transaction - prioritize completed, then pending
    payment_transaction = None
    pending_txn_id = request.session.get('pending_payment_transaction_id')
    if pending_txn_id:
        try:
            payment_transaction = models.PaymentTransaction.objects.get(id=pending_txn_id, user=request.user)
        except models.PaymentTransaction.DoesNotExist:
            pass
    
    # If not found in session, get from database - prioritize completed transactions
    if not payment_transaction:
        # First try to get completed transaction (if payment is verified)
        if request.user.payment_done:
            payment_transaction = models.PaymentTransaction.objects.filter(
                user=request.user,
                payment_status='completed'
            ).order_by('-verified_at', '-created_at').first()
        
        # If no completed transaction, get pending
        if not payment_transaction:
            payment_transaction = models.PaymentTransaction.objects.filter(
                user=request.user,
                payment_status='pending'
            ).order_by('-created_at').first()
    
    # Create new transaction if doesn't exist (only if payment not done)
    if not payment_transaction and not request.user.payment_done:
        import uuid
        transaction_id = f"TXN{request.user.phone_number}{uuid.uuid4().hex[:8].upper()}"
        payment_transaction = models.PaymentTransaction.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            amount=500.00,
            payment_status='pending'
        )
        # Store in session
        request.session['pending_payment_transaction_id'] = payment_transaction.id
        request.session.save()
    
    # Check payment status
    payment_pending = False
    if payment_transaction and payment_transaction.payment_status == 'pending':
        payment_pending = True
    
    context = {
        'user_avatar': user_avatar,
        'username': username,
        'payment_transaction': payment_transaction,
        'payment_amount': float(payment_transaction.amount) if payment_transaction else 500.00,
        'payment_done': request.user.payment_done,
        'payment_pending': payment_pending,
        'pending_transaction': payment_transaction if payment_pending else None,
    }
    # Payment status is also added via context processor
    
    return render(request, 'payment.html', context)


def verify_payment(request):
    """Verify payment and update user payment status"""
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                transaction_id = data.get('transaction_id')
                payment_proof = None
            else:
                transaction_id = request.POST.get('transaction_id')
                payment_proof = request.FILES.get('payment_proof') if request.FILES else None
            
            if not transaction_id:
                return JsonResponse({'success': False, 'message': 'Transaction ID is required'}, status=400)
            
            transaction = models.PaymentTransaction.objects.filter(transaction_id=transaction_id).first()
            
            if not transaction:
                return JsonResponse({'success': False, 'message': 'Transaction not found'}, status=404)
            
            # Update transaction with payment proof
            if payment_proof:
                transaction.payment_proof = payment_proof
                transaction.payment_status = 'pending'  # Admin needs to verify
                transaction.save()
                # Notify admin (mark as notified)
                if not transaction.admin_notified:
                    transaction.notify_admin()
            else:
                # If no proof uploaded, mark as pending for admin verification
                transaction.payment_status = 'pending'
                transaction.save()
                # Notify admin
                if not transaction.admin_notified:
                    transaction.notify_admin()
            
            # Clear session
            if 'pending_payment_user_id' in request.session:
                del request.session['pending_payment_user_id']
            if 'pending_payment_transaction_id' in request.session:
                del request.session['pending_payment_transaction_id']
            
            return JsonResponse({
                'success': True, 
                'message': 'Payment proof uploaded successfully. Your payment is under verification. You will get access once admin verifies your payment.',
                'status': 'pending'
            }, status=200)
                
        except Exception as e:
            print(f"Error verifying payment: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def check_payment_status(request):
    """Check if user has completed payment"""
    if request.user.is_authenticated:
        return JsonResponse({
            'success': True,
            'payment_done': request.user.payment_done,
            'message': 'Payment completed' if request.user.payment_done else 'Payment pending'
        })
    return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=401)
