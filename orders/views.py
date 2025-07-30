from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderForm
from store.models import Product
from payment.models import Payment
import uuid

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'orders/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is available and in stock
    if not product.is_available or product.stock <= 0:
        messages.error(request, "Sorry, this product is not available or out of stock.")
        return redirect('store:product_detail', product_slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get quantity from form
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if quantity is valid
    if quantity <= 0:
        quantity = 1
    if quantity > product.stock:
        quantity = product.stock
    
    # Check if product already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"'{product.name}' quantity updated in your cart.")
    except CartItem.DoesNotExist:
        # Add new item to cart
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f"'{product.name}' added to your cart.")
    
    return redirect('orders:cart_detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f"'{product.name}' removed from your cart.")
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    
    return redirect('orders:cart_detail')

@login_required
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"'{product.name}' removed from your cart.")
        else:
            if quantity > product.stock:
                quantity = product.stock
                messages.warning(request, f"Only {product.stock} of '{product.name}' available.")
            
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"'{product.name}' quantity updated.")
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    
    return redirect('orders:cart_detail')

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(request, "Your cart is empty. Please add some products before checkout.")
            return redirect('orders:cart_detail')
        
        # Check stock availability
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Only {item.product.stock} of '{item.product.name}' available. Please update your cart.")
                return redirect('orders:cart_detail')
        
        # Calculate total
        total_price = cart.get_total_price()
        
        if request.method == 'POST':
            form = OrderForm(request.POST)
            
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = total_price
                order.save()
                
                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity
                    )
                    
                    # Update product stock
                    item.product.stock = F('stock') - item.quantity
                    item.product.save()
                
                # Clear cart
                cart.items.all().delete()
                
                # Redirect to payment page
                return redirect('payment:payment_process', tracking_number=order.tracking_number)
        else:
            # Pre-fill form with user data
            initial_data = {}
            if request.user.first_name:
                initial_data['first_name'] = request.user.first_name
            if request.user.last_name:
                initial_data['last_name'] = request.user.last_name
            if request.user.email:
                initial_data['email'] = request.user.email
            if request.user.phone_number:
                initial_data['phone'] = request.user.phone_number
            if request.user.address:
                initial_data['address'] = request.user.address
            
            form = OrderForm(initial=initial_data)
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'form': form
        }
        return render(request, 'orders/checkout.html', context)
    
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty. Please add some products before checkout.")
        return redirect('store:home')

@login_required
def order_complete(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'order': order,
        'payment': payment,
        'order_items': order.items.all()
    }
    return render(request, 'orders/order_complete.html', context)

@login_required
def track_order(request):
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number', '')
        return redirect('orders:track_order_detail', tracking_number=tracking_number)
    
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_orders': recent_orders
    }
    return render(request, 'orders/track_order.html', context)

def track_order_detail(request, tracking_number):
    try:
        # If user is logged in, make sure they can only see their own orders
        if request.user.is_authenticated:
            order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
        else:
            order = get_object_or_404(Order, tracking_number=tracking_number)
        
        context = {
            'order': order,
            'order_items': order.items.all()
        }
        return render(request, 'orders/track_order_detail.html', context)
    
    except:
        messages.error(request, "Invalid tracking number. Please try again.")
        return redirect('orders:track_order')