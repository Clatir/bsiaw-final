from django.http import HttpResponseForbidden
from .models import UserProfile

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != required_role:
                return HttpResponseForbidden("Nie masz dostępu do tej strony.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator