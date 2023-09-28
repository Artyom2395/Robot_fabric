from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Access denied. This action requires admin privileges.'}, status=403)
    return _wrapped_view

def director_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Проверяем, является ли текущий пользователь директором
        if request.user.is_authenticated and request.user.director.is_director:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied: You are not a director.")

    return _wrapped_view