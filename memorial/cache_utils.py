"""Shared cache keys and invalidation for read-heavy public memorial pages."""

import os

from django.core.cache import cache

GALLERY_LIST_KEY = "memorial:gallery_ordered_v1"
VISIT_DESTINATIONS_KEY = "memorial:visit_destinations_v1"
FEATURED_QUOTE_OBJECT_KEY = "memorial:featured_quote_obj_v1"
HOME_CONTENT_OBJECT_KEY = "memorial:home_content_obj_v1"
HOME_CONTENT_PK_KEY = "memorial:home_content_pk_v1"
LIFE_CHAPTERS_LIST_KEY = "memorial:life_chapters_v1"
LIFE_STORY_PAGE_KEY = "memorial:life_story_page_v1"
TRIBUTES_PAGE_KEY = "memorial:tributes_page_v1"
HOME_PROGRAMME_PREFIX = "memorial:home_programme_v2"
HEALTH_DB_OK_KEY = "memorial:health_db_ok_v1"

PUBLIC_CACHE_SECONDS = int(os.getenv("PUBLIC_CACHE_SECONDS", "600"))
HEALTH_CACHE_SECONDS = int(os.getenv("HEALTH_CACHE_SECONDS", "5"))


def invalidate_gallery_cache():
    cache.delete(GALLERY_LIST_KEY)


def invalidate_visit_cache():
    cache.delete(VISIT_DESTINATIONS_KEY)


def invalidate_home_content_cache():
    cache.delete(HOME_CONTENT_OBJECT_KEY)
    cache.delete(HOME_CONTENT_PK_KEY)


def invalidate_featured_quote_cache():
    cache.delete(FEATURED_QUOTE_OBJECT_KEY)


def invalidate_life_chapters_cache():
    cache.delete(LIFE_CHAPTERS_LIST_KEY)
    cache.delete(LIFE_STORY_PAGE_KEY)


def invalidate_tributes_cache():
    cache.delete(TRIBUTES_PAGE_KEY)


def invalidate_public_content_caches():
    invalidate_home_content_cache()
    invalidate_featured_quote_cache()
    invalidate_visit_cache()
    invalidate_gallery_cache()
    invalidate_life_chapters_cache()
    invalidate_tributes_cache()
