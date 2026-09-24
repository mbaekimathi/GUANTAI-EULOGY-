from django.conf import settings
from django.core.checks import Warning, register

_INSECURE_SECRET_PREFIX = "django-insecure-"


@register()
def memorial_production_safety(app_configs, **kwargs):
    if settings.DEBUG:
        return []

    warnings = []
    secret = getattr(settings, "SECRET_KEY", "") or ""
    if secret.startswith(_INSECURE_SECRET_PREFIX):
        warnings.append(
            Warning(
                "DJANGO_SECRET_KEY is still the development default.",
                hint="Set a unique DJANGO_SECRET_KEY in the environment before going live.",
                id="memorial.W001",
            )
        )

    default_password = "123456789"
    if getattr(settings, "MEMORIAL_ADMIN_PASSWORD", None) == default_password:
        warnings.append(
            Warning(
                "Memorial dashboard password is still the default.",
                hint="Set MEMORIAL_ADMIN_PASSWORD in the environment to a strong secret.",
                id="memorial.W002",
            )
        )

    if getattr(settings, "USE_SQLITE", False):
        warnings.append(
            Warning(
                "SQLite is enabled in production — concurrent traffic will bottleneck on writes.",
                hint="Set USE_SQLITE=False and configure MySQL (see README) before a high-traffic event.",
                id="memorial.W003",
            )
        )

    return warnings
