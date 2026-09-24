"""
Django settings for the Fredrick Guantai Mugira memorial site.
"""

import os
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
    "memorial",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "memorial.context_processors.memorial_navigation",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() in ("1", "true", "yes")

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

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
