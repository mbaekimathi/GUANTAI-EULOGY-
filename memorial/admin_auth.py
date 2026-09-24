from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

SESSION_KEY = "memorial_admin_authenticated"


def is_memorial_admin(request):
    return request.session.get(SESSION_KEY) is True


def memorial_admin_login(request):
    request.session[SESSION_KEY] = True
    request.session.modified = True


def memorial_admin_logout(request):
    request.session.pop(SESSION_KEY, None)
    request.session.modified = True


def credentials_valid(username, password):
    return (
        username == settings.MEMORIAL_ADMIN_USERNAME
        and password == settings.MEMORIAL_ADMIN_PASSWORD
    )


def require_memorial_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_memorial_admin(request):
            return redirect(
                f"{reverse('memorial:dashboard_login')}?next={request.path}"
            )
        return view_func(request, *args, **kwargs)

    return wrapper
