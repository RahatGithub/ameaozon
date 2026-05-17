from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps


def admin_required(view_func):
    """Must be stacked below @login_required (which handles unauthenticated users)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == 'admin' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Admin privileges required.")
        return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapper