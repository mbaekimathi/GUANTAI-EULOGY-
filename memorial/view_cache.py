from functools import wraps

from django.utils.cache import patch_cache_control

from .admin_auth import is_memorial_admin

DEFAULT_PUBLIC_MAX_AGE = 120


def cache_public_get(max_age=DEFAULT_PUBLIC_MAX_AGE):
    """Allow CDN/browser caching for anonymous visitors; never cache admin sessions."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if request.method != "GET" or is_memorial_admin(request):
                patch_cache_control(response, no_cache=True, no_store=True, private=True)
            else:
                patch_cache_control(
                    response,
                    public=True,
                    max_age=max_age,
                    stale_while_revalidate=max_age * 5,
                )
            return response

        return wrapper

    return decorator
