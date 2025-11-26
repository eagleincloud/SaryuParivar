"""
Context processor to add payment status to all dashboard templates
"""
from administration import models as admin_models

def payment_status(request):
    """Add payment status to all dashboard templates"""
    if request.user.is_authenticated and not request.user.is_superuser:
        payment_pending = False
        pending_transaction = None
        
        if not request.user.payment_done:
            pending_transaction = admin_models.PaymentTransaction.objects.filter(
                user=request.user,
                payment_status='pending'
            ).first()
            if pending_transaction:
                payment_pending = True
        
        return {
            'payment_pending': payment_pending,
            'pending_transaction': pending_transaction,
            'payment_done': request.user.payment_done,
        }
    return {
        'payment_pending': False,
        'pending_transaction': None,
        'payment_done': True,
    }

