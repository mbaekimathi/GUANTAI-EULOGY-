from django.urls import path

from django.views.generic.base import RedirectView



from . import dashboard_views, views



app_name = "memorial"



urlpatterns = [

    path("health/", views.health, name="health"),

    path("", views.home, name="home"),

    path("home/", RedirectView.as_view(pattern_name="memorial:home", permanent=False)),

    path("life-story/", views.life_story, name="life_story"),

    path("life/", RedirectView.as_view(pattern_name="memorial:life_story", permanent=False)),

    path("legacy/", views.legacy, name="legacy"),

    path("family/", views.family, name="family"),

    path("tributes/", views.tributes, name="tributes"),

    path("gallery/", views.gallery, name="gallery"),

    path("service/", views.service, name="service"),

    path("visit/", views.visit, name="visit"),

    path("visit/go/<slug:place>/", views.visit_go, name="visit_go"),

    path("dashboard/", dashboard_views.dashboard_home, name="dashboard_home"),

    path(
        "dashboard/home/",
        dashboard_views.dashboard_home_update,
        name="dashboard_home_update",
    ),

    path("dashboard/login/", dashboard_views.dashboard_login, name="dashboard_login"),

    path("dashboard/logout/", dashboard_views.dashboard_logout, name="dashboard_logout"),

    path(
        "dashboard/life-story/",
        dashboard_views.dashboard_life_story,
        name="dashboard_life_story",
    ),

    path(

        "dashboard/tributes/",

        dashboard_views.dashboard_tributes,

        name="dashboard_tributes",

    ),

    path("dashboard/gallery/", dashboard_views.dashboard_gallery, name="dashboard_gallery"),

    path(
        "dashboard/gallery/<int:pk>/edit/",
        dashboard_views.dashboard_gallery_edit,
        name="dashboard_gallery_edit",
    ),

    path(

        "dashboard/location/",

        dashboard_views.dashboard_location,

        name="dashboard_location",

    ),

]

