from django.conf import settings
from django.http import Http404

from django.shortcuts import redirect, render

from django.views.decorators.cache import never_cache

from django.views.decorators.http import require_http_methods



from .content_data import (

    eulogy_body_paragraphs,

    get_approved_tributes,

    get_eulogy_content,

    get_gallery_photos,

    get_home_page_content,

    parse_programme_service,

    parse_programme_timeline,

    build_life_story_items,

    build_tribute_items,

    get_life_chapters,

    get_visit_destinations,

    resolve_visit_maps_query,

)


from .maps import google_maps_directions_url

from .models import MemorialQuote





def _visit_destinations():

    return get_visit_destinations()





@never_cache

def home(request):

    home_content = get_home_page_content()

    quote = MemorialQuote.objects.filter(is_active=True).first()

    gallery_preview = get_gallery_photos()[:4]

    return render(

        request,

        "memorial/home.html",

        {

            "page_title": "In Loving Memory",

            "home_content": home_content,

            "programme_timeline": parse_programme_timeline(home_content.programme_timeline),

            "programme_service": parse_programme_service(home_content.programme_service),

            "featured_quote": quote,

            "gallery_preview": gallery_preview,

        },

    )





@never_cache

def eulogy(request):

    content = get_eulogy_content()

    hero_lead = getattr(content, "hero_lead", None) or content.get("hero_lead", "")

    closing_prayer = getattr(content, "closing_prayer", None) or content.get(

        "closing_prayer", ""

    )

    return render(

        request,

        "memorial/eulogy.html",

        {

            "page_title": "Eulogy",

            "eulogy_hero_lead": hero_lead,

            "eulogy_paragraphs": eulogy_body_paragraphs(content),

            "eulogy_closing_prayer": closing_prayer,

        },

    )





@never_cache

def life_story(request):

    chapters = get_life_chapters()
    memorial = settings.MEMORIAL
    birth = memorial.get("birth_year", 1930)
    death = memorial.get("death_year", birth)
    memorial_years = max(0, death - birth)

    return render(

        request,

        "memorial/life_story.html",

        {
            "page_title": "Life Story",
            "story_items": build_life_story_items(chapters),
            "memorial_years": memorial_years,
        },

    )





@never_cache

def legacy(request):

    return render(

        request,

        "memorial/legacy.html",

        {"page_title": "Legacy & Values"},

    )





@never_cache

def family(request):

    return render(

        request,

        "memorial/family.html",

        {"page_title": "Family & Gratitude"},

    )





@never_cache

@require_http_methods(["GET"])

def tributes(request):

    tribute_list = get_approved_tributes()

    return render(

        request,

        "memorial/tributes.html",

        {

            "page_title": "Tributes & Memories",

            "tributes": tribute_list,

            "tribute_items": build_tribute_items(tribute_list),

        },

    )





@never_cache

def service(request):

    return render(

        request,

        "memorial/service.html",

        {"page_title": "Memorial Service"},

    )





@never_cache

def visit(request):

    return render(

        request,

        "memorial/visit.html",

        {

            "page_title": "Visit & Directions",

            "visit_destinations": _visit_destinations(),

        },

    )





def visit_go(request, place):

    maps_query = resolve_visit_maps_query(place)

    if not maps_query:

        raise Http404("Unknown visit location")

    url = google_maps_directions_url(maps_query)

    return redirect(url)





@never_cache

def gallery(request):

    photos = get_gallery_photos()

    return render(

        request,

        "memorial/gallery.html",

        {"page_title": "Gallery", "photos": photos},

    )


