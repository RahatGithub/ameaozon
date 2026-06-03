from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import User
from .forms import UserRegisterForm, UserUpdateForm
from store.models import Wishlist


def login_view(request):
    """Handle user login with proper toast messages."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'store:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html')


@require_POST
def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('store:home')


def register(request):
    """Handle new user registration with username and email."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please fix the errors below to create your account.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """Display and update user profile information."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Could not update your profile. Please fix the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def customer_dashboard(request):
    """Show customer's orders and wishlist; redirect admins to admin dashboard."""
    if request.user.user_type == User.ADMIN:
        return redirect('dashboard:admin_dashboard')

    orders = request.user.orders.all().order_by('-created_at')
    wishlist = Wishlist.objects.filter(user=request.user).first()

    context = {
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request, 'accounts/customer_dashboard.html', context)
