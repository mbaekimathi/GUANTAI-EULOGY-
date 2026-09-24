from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

SESSION_KEY = "memorial_admin_authenticated"


def is_memorial_admin(request):
    """Skip loading the session store when the browser has no session cookie."""
    if not request.COOKIES.get(settings.SESSION_COOKIE_NAME):
        return False
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


def safe_admin_redirect_target(next_url, request):
    """Only allow same-site relative paths after login (blocks //evil.com open redirects)."""
    if not next_url:
        return None
    if url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def require_memorial_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_memorial_admin(request):
            return redirect(
                f"{reverse('memorial:dashboard_login')}?next={request.path}"
            )
        return view_func(request, *args, **kwargs)

    return wrapper
