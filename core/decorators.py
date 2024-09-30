# core/decorators.py

from django.http import HttpResponseForbidden
from functools import wraps
from .models import Role, Profile

def permission_required(permission_name):
    """
    Decorator to check if the user has the specified permission.
    :param permission_name: Name of the permission to check.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            profile = Profile.objects.get(user=request.user)
            user_role = profile.role  # Modify as necessary            
            try:
                role_permission = Role.objects.get(role_name=user_role)
            except Role.DoesNotExist:
                return HttpResponseForbidden("You do not have permission to access this resource.")

            
            if getattr(role_permission, permission_name, False):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        
        return _wrapped_view
    return decorator

def permissions_required(*permission_names):


    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            profile = Profile.objects.get(user=request.user)
            user_role = profile.role  # Modify as necessary
            try:
                role_permission = Role.objects.get(role_name=user_role)
            except Role.DoesNotExist:
                return HttpResponseForbidden("You do not have permission to access this resource.")

            for permission_name in permission_names:
                if not getattr(role_permission, permission_name, False):
                    return HttpResponseForbidden("You do not have permission to access this resource.")
                    
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
