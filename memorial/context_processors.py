from functools import lru_cache

from django.conf import settings
from django.urls import reverse

from .admin_auth import is_memorial_admin



DASHBOARD_NAV = [

    ("dashboard", "Dashboard", "dashboard_home"),

    ("home", "Home page", "dashboard_home_update"),

    ("life", "Life story", "dashboard_life_story"),

    ("tributes", "Tributes", "dashboard_tributes"),

    ("gallery", "Gallery", "dashboard_gallery"),

    ("location", "Locations", "dashboard_location"),

]



PUBLIC_NAV = [

    ("home", "Home", "home"),

    ("life", "Life Story", "life_story"),

    ("legacy", "Legacy", "legacy"),

    ("tributes", "Tributes", "tributes"),

    ("gallery", "Gallery", "gallery"),

    ("visit", "Visit", "visit"),

]





def _nav_items(raw_items):
    return [
        {
            "slug": slug,
            "label": label,
            "url_name": url_name,
            "href": reverse(f"memorial:{url_name}"),
            "icon": slug,
        }
        for slug, label, url_name in raw_items
    ]


@lru_cache(maxsize=1)
def _cached_public_nav_items():
    return _nav_items(PUBLIC_NAV)


@lru_cache(maxsize=1)
def _cached_dashboard_nav_items():
    return _nav_items(DASHBOARD_NAV)





def memorial_navigation(request):

    memorial = settings.MEMORIAL

    is_admin_dashboard = False

    active = ""

    if request.resolver_match and request.resolver_match.namespace == "memorial":

        active = request.resolver_match.url_name or ""

        is_admin_dashboard = active.startswith("dashboard_")



    nav_items = (
        _cached_dashboard_nav_items()
        if is_admin_dashboard
        else _cached_public_nav_items()
    )

    if is_admin_dashboard or request.COOKIES.get(settings.SESSION_COOKIE_NAME):
        is_memorial_admin_flag = is_memorial_admin(request)
    else:
        is_memorial_admin_flag = False

    return {
        "memorial": memorial,
        "nav_items": nav_items,
        "nav_active": active,
        "is_admin_dashboard": is_admin_dashboard,
        "is_memorial_admin": is_memorial_admin_flag,
        "home_url": reverse("memorial:home"),
    }

