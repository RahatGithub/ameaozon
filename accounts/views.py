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
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Ameaozon, {user.username}!')
            return redirect('store:home')
        else:
            messages.error(request, 'Please fix the errors below to create your account.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def admin_login_view(request):
    """Handle admin-only login with separate UI."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser or request.user.is_admin():
            return redirect('/admin/')
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'accounts/admin_login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser or user.is_admin():
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('/admin/')
            else:
                messages.error(request, 'You are not an admin. Try using the <a href="/accounts/login/" class="font-semibold text-brand-600 hover:text-brand-700">user login form</a>.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/admin_login.html')


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
