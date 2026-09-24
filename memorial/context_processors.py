from django.conf import settings

from django.urls import reverse



DASHBOARD_NAV = [

    ("dashboard", "Dashboard", "dashboard_home"),

    ("home", "Home page", "dashboard_home_update"),

    ("eulogy", "Eulogy", "dashboard_eulogy"),

    ("life", "Life story", "dashboard_life_story"),

    ("tributes", "Tributes", "dashboard_tributes"),

    ("gallery", "Gallery", "dashboard_gallery"),

    ("location", "Locations", "dashboard_location"),

]



PUBLIC_NAV = [

    ("home", "Home", "home"),

    ("eulogy", "Eulogy", "eulogy"),

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





def memorial_navigation(request):

    memorial = settings.MEMORIAL

    is_admin_dashboard = False

    active = ""

    if request.resolver_match and request.resolver_match.namespace == "memorial":

        active = request.resolver_match.url_name or ""

        is_admin_dashboard = active.startswith("dashboard_")



    raw_items = DASHBOARD_NAV if is_admin_dashboard else PUBLIC_NAV

    nav_items = _nav_items(raw_items)



    return {

        "memorial": memorial,

        "nav_items": nav_items,

        "nav_active": active,

        "is_admin_dashboard": is_admin_dashboard,

        "home_url": reverse("memorial:home"),

    }

