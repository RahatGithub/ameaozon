from django.shortcuts import redirect


class AdminRedirectMiddleware:
    """Redirect admin users away from customer-facing pages to the dashboard."""

    ALLOWED_PREFIXES = (
        '/dashboard/',
        '/admin/',
        '/staff/',
        '/accounts/logout/',
        '/accounts/profile/',
        '/media/',
        '/static/',
        '/health/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and hasattr(request.user, 'is_admin')
            and request.user.is_admin()
            and not any(request.path.startswith(p) for p in self.ALLOWED_PREFIXES)
        ):
            return redirect('dashboard:admin_dashboard')

        return self.get_response(request)
