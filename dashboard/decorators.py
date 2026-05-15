from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.user.user_type == 'admin' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Admin privileges required.")
        return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapper