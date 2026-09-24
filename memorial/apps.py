from django.apps import AppConfig


class MemorialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "memorial"

    def ready(self):
        from django.db.models.signals import post_delete, post_save

        from . import checks  # noqa: F401
        from .cache_utils import (
            invalidate_featured_quote_cache,
            invalidate_gallery_cache,
            invalidate_home_content_cache,
            invalidate_life_chapters_cache,
            invalidate_tributes_cache,
            invalidate_visit_cache,
        )
        from .models import (
            GalleryImage,
            HomePageContent,
            LifeChapter,
            MemorialQuote,
            Tribute,
            VisitLocation,
        )

        post_save.connect(lambda **_: invalidate_gallery_cache(), sender=GalleryImage)
        post_delete.connect(lambda **_: invalidate_gallery_cache(), sender=GalleryImage)
        post_save.connect(lambda **_: invalidate_home_content_cache(), sender=HomePageContent)
        post_save.connect(lambda **_: invalidate_featured_quote_cache(), sender=MemorialQuote)
        post_delete.connect(lambda **_: invalidate_featured_quote_cache(), sender=MemorialQuote)
        post_save.connect(lambda **_: invalidate_life_chapters_cache(), sender=LifeChapter)
        post_delete.connect(lambda **_: invalidate_life_chapters_cache(), sender=LifeChapter)
        post_save.connect(lambda **_: invalidate_visit_cache(), sender=VisitLocation)
        post_delete.connect(lambda **_: invalidate_visit_cache(), sender=VisitLocation)
        post_save.connect(lambda **_: invalidate_tributes_cache(), sender=Tribute)
        post_delete.connect(lambda **_: invalidate_tributes_cache(), sender=Tribute)
