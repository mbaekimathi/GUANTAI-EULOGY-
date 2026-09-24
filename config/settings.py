"""
Django settings for the Fredrick Guantai Mugira memorial site.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-change-before-production",
)
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")
_DEFAULT_ALLOWED_HOSTS = "localhost,127.0.0.1,guantai.projectlucas.co.ke"
_allowed_raw = os.getenv("ALLOWED_HOSTS", "").strip() or _DEFAULT_ALLOWED_HOSTS
ALLOWED_HOSTS = [h.strip() for h in _allowed_raw.split(",") if h.strip()]

_DEFAULT_CSRF_ORIGINS = "https://guantai.projectlucas.co.ke"
_csrf_raw = os.getenv("CSRF_TRUSTED_ORIGINS", "").strip() or _DEFAULT_CSRF_ORIGINS
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_raw.split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "memorial.apps.MemorialConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "memorial.context_processors.memorial_navigation",
]
if DEBUG:
    _TEMPLATE_CONTEXT_PROCESSORS.insert(
        0, "django.template.context_processors.debug"
    )

_TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
if not DEBUG and "test" not in sys.argv:
    _TEMPLATE_LOADERS = [
        ("django.template.loaders.cached.Loader", _TEMPLATE_LOADERS),
    ]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": not (not DEBUG and "test" not in sys.argv),
        "OPTIONS": {
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
            **(
                {"loaders": _TEMPLATE_LOADERS}
                if not DEBUG and "test" not in sys.argv
                else {}
            ),
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() in ("1", "true", "yes")

_CONN_MAX_AGE = int(os.getenv("DB_CONN_MAX_AGE", "600"))

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "OPTIONS": {
                "timeout": int(os.getenv("SQLITE_TIMEOUT", "30")),
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "guantai_memorial"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "CONN_MAX_AGE": _CONN_MAX_AGE,
            "CONN_HEALTH_CHECKS": True,
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

_CACHE_DIR = Path(os.getenv("CACHE_DIR", str(BASE_DIR / "var" / "cache")))
_CACHE_DIR.mkdir(parents=True, exist_ok=True)

if "test" in sys.argv:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "memorial-tests",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": os.getenv(
                "CACHE_BACKEND",
                "django.core.cache.backends.filebased.FileBasedCache",
            ),
            "LOCATION": str(_CACHE_DIR),
            "TIMEOUT": int(os.getenv("CACHE_TIMEOUT", os.getenv("PUBLIC_CACHE_SECONDS", "600"))),
            "OPTIONS": {"MAX_ENTRIES": int(os.getenv("CACHE_MAX_ENTRIES", "10000"))},
        }
    }

# Signed cookies: no session DB write per anonymous visitor (best for read-heavy traffic).
SESSION_ENGINE = os.getenv(
    "SESSION_ENGINE",
    "django.contrib.sessions.backends.signed_cookies",
)
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = int(os.getenv("SESSION_COOKIE_AGE", str(60 * 60 * 24 * 14)))
SESSION_SAVE_EVERY_REQUEST = False

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

WHITENOISE_MAX_AGE = int(os.getenv("WHITENOISE_MAX_AGE", str(60 * 60 * 24 * 30)))
WHITENOISE_INDEX_FILE = True
WHITENOISE_USE_FINDERS = DEBUG

if USE_SQLITE:
    from config.sqlite import enable_sqlite_wal

    enable_sqlite_wal()

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    if os.getenv("DJANGO_USE_HTTPS", "True").lower() in ("1", "true", "yes"):
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEMORIAL_ADMIN_USERNAME = os.getenv("MEMORIAL_ADMIN_USERNAME", "987654321")
MEMORIAL_ADMIN_PASSWORD = os.getenv("MEMORIAL_ADMIN_PASSWORD", "123456789")

MEMORIAL = {
    "full_name": "Fredrick Guantai Mugira",
    "short_name": "Mzee Fredrick",
    "birth_year": 1930,
    "death_year": 2026,
    "death_date_display": "17 September 2026",
    "burial_date_display": "Thursday, 25 September 2026",
    "burial_date_short": "25 September 2026",
    "burial_venue": "PCEA Mbogori Church, Chogoria",
    "birth_place": "Meru County, Kenya",
    "tagline": "A life rooted in faith, family, and quiet strength.",
}

# Update labels and map queries with the family's exact venues.
MEMORIAL_VISIT = {
    "church": {
        "slug": "church",
        "title": "Church",
        "subtitle": "Service & prayers",
        "place_name": "PCEA Mbogori Church, Chogoria",
        # Google Maps pin (Mbogori Primary School / church area)
        "maps_query": "-0.2002388,37.6044681",
    },
    "home": {
        "slug": "home",
        "title": "Family home",
        "subtitle": "Viewing & gathering",
        "place_name": "Mugira–Guantai family home",
        "maps_query": "-0.2002388,37.6044681",
    },
}
