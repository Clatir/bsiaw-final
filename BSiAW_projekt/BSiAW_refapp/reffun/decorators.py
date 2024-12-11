from django.http import HttpResponseForbidden
from authentication.models import UserProfile
from django.shortcuts import get_object_or_404
from functools import wraps
from game.models import Match

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != required_role:
                return HttpResponseForbidden("Nie masz dostępu do tej strony.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def referee_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        match = get_object_or_404(Match, id=kwargs['mecz_id'])
        if match.SedziaG != profile.user:
            return HttpResponseForbidden("Nie masz dostępu do tego meczu.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    

def referees_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        match = get_object_or_404(Match, id=kwargs['mecz_id'])
        if match.SedziaG != profile.user and match.SedziaA1 != profile.user and match.SedziaA2 != profile.user:
            return HttpResponseForbidden("Nie masz dostępu do tego meczu.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
