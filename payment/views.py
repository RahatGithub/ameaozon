from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from orders.models import Order
from .models import Payment
import uuid
import random
import string

@login_required
def payment_process(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    
    # If order is already paid, redirect to order detail
    if order.payment_completed:
        messages.info(request, "This order has already been paid for.")
        return redirect('orders:order_complete', tracking_number=order.tracking_number)
    
    # Handle Cash on Delivery
    if order.payment_method == 'cash_on_delivery':
        # Create payment record for COD
        payment = Payment.objects.create(
            order=order,
            payment_id=f"COD-{order.tracking_number}",
            amount=order.total_price,
            status='pending',
            payment_method='Cash on Delivery'
        )
        
        # Update order but don't mark as paid yet
        order.status = 'processing'
        order.save()
        
        return redirect('payment:payment_complete', tracking_number=order.tracking_number)
    
    # For other payment methods
    context = {
        'order': order,
        'payment_method': order.get_payment_method_display()
    }
    return render(request, 'payment/payment_process.html', context)

@login_required
def payment_complete(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    
    # For online payment methods (when payment form submitted)
    if request.method == 'POST' and order.payment_method != 'cash_on_delivery':
        # Simulate payment process (in a real app, this would interact with a payment gateway)
        payment_successful = True  # Always assume success for demo
        
        if payment_successful:
            # Generate a random payment ID
            payment_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                payment_id=payment_id,
                amount=order.total_price,
                status='completed',
                payment_method=order.get_payment_method_display()
            )
            
            # Update order
            order.payment_completed = True
            order.status = 'processing'
            order.save()
            
            messages.success(request, "Payment completed successfully!")
            return redirect('orders:order_complete', tracking_number=order.tracking_number)
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('payment:payment_process', tracking_number=order.tracking_number)
    
    # For Cash on Delivery or to show payment confirmation page
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'order': order,
        'payment': payment
    }
    return render(request, 'payment/payment_complete.html', context)

@login_required
def payment_canceled(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    
    messages.warning(request, "Your payment was canceled.")
    
    context = {
        'order': order
    }
    return render(request, 'payment/payment_canceled.html', context)