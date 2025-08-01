from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm



def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('store:home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def customer_dashboard(request):
    if request.user.user_type == User.ADMIN:
        return redirect('dashboard:admin_dashboard')
    
    orders = request.user.orders.all().order_by('-created_at')
    try:
        wishlist = request.user.wishlist_set.first()
    except:
        wishlist = None
    
    context = {
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request, 'accounts/customer_dashboard.html', context)
