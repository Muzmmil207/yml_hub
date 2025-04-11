from django.shortcuts import redirect
from django.urls import reverse


class RedirectParentToDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = [
            reverse('profile'),
            reverse('login'),
            reverse('logout'),
            reverse('parent-dashboard'),
        ]

    def __call__(self, request):
        user = request.user
        path = request.path

        if user.is_authenticated and getattr(user, 'role', None) == 'parent':
            # Avoid redirect loop
            if not any(path.startswith(p) for p in self.allowed_paths) and not path.startswith('/admin/'):
                return redirect('parent-dashboard')

        return self.get_response(request)
