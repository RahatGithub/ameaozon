from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # সুপারইউজারদের অ্যাকসেস দেওয়ার জন্য is_superuser চেক যুক্ত করা হয়েছে
        if request.user.is_authenticated and (request.user.user_type == 'admin' or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            # messages.error(request, "Access denied. Admin privileges required.")
            return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapper