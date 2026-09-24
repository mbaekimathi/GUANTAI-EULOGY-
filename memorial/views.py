from django.core.cache import cache
from django.db import connection
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .cache_utils import HEALTH_CACHE_SECONDS, HEALTH_DB_OK_KEY
from .content_data import (
    build_home_page_context,
    get_gallery_photos_display,
    get_life_story_page_context,
    get_tributes_page_context,
    get_visit_destinations,
    resolve_visit_maps_query,
)
from .maps import google_maps_directions_url
from .view_cache import cache_public_get


@require_GET
def health(request):
    """Load-balancer probe; DB check cached briefly to avoid hammering under poll traffic."""
    try:
        if cache.get(HEALTH_DB_OK_KEY):
            return JsonResponse({"status": "ok"})
    except Exception:
        pass
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        return JsonResponse({"status": "error"}, status=503)
    try:
        cache.set(HEALTH_DB_OK_KEY, True, HEALTH_CACHE_SECONDS)
    except Exception:
        pass
    return JsonResponse({"status": "ok"})


@cache_public_get(max_age=120)
def home(request):
    context = build_home_page_context(request)
    return render(
        request,
        "memorial/home.html",
        {
            "page_title": "In Loving Memory",
            **context,
        },
    )


@cache_public_get(max_age=300)
def life_story(request):
    return render(
        request,
        "memorial/life_story.html",
        {
            "page_title": "Life Story",
            **get_life_story_page_context(),
        },
    )


@cache_public_get(max_age=600)
def legacy(request):
    return render(
        request,
        "memorial/legacy.html",
        {"page_title": "Legacy & Values"},
    )


@cache_public_get(max_age=600)
def family(request):
    return render(
        request,
        "memorial/family.html",
        {"page_title": "Family & Gratitude"},
    )


@cache_public_get(max_age=120)
@require_http_methods(["GET"])
def tributes(request):
    return render(
        request,
        "memorial/tributes.html",
        {
            "page_title": "Tributes & Memories",
            **get_tributes_page_context(),
        },
    )


@cache_public_get(max_age=600)
def service(request):
    return render(
        request,
        "memorial/service.html",
        {"page_title": "Memorial Service"},
    )


@cache_public_get(max_age=300)
def visit(request):
    return render(
        request,
        "memorial/visit.html",
        {
            "page_title": "Visit & Directions",
            "visit_destinations": get_visit_destinations(),
        },
    )


def visit_go(request, place):
    maps_query = resolve_visit_maps_query(place)
    if not maps_query:
        raise Http404("Unknown visit location")
    url = google_maps_directions_url(maps_query)
    return redirect(url)


@cache_public_get(max_age=120)
def gallery(request):
    photos = get_gallery_photos_display(request)
    return render(
        request,
        "memorial/gallery.html",
        {"page_title": "Gallery", "photos": photos},
    )
