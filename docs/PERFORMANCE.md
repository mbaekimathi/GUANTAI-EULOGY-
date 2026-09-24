# Performance & capacity

This site is tuned for **many simultaneous read-only visitors** (funeral programme, gallery, tributes).

## Architecture (defaults)

| Layer | Setting | Why |
|--------|---------|-----|
| Database (production) | MySQL, `CONN_MAX_AGE=600` | Connection reuse across requests |
| Database (local only) | SQLite + WAL | Dev convenience; not for high traffic |
| Sessions | `signed_cookies` | No session DB row per anonymous visitor |
| App cache | File cache in `var/cache/` | Shared across Passenger workers on one server |
| Public content | 600s object cache | Home, gallery, life story, tributes, visit maps |
| Static files | WhiteNoise compressed + 30-day browser cache | After `collectstatic` |
| HTML | GZip + short `Cache-Control` for anonymous GETs | CDN/browser friendly |
| Templates | Cached loader when `DEBUG=False` | Less CPU per request |

## Before a high-traffic event

```bash
python manage.py migrate
python manage.py seed_memorial
python manage.py collectstatic --noinput
python manage.py check --deploy
python manage.py stress_test --workers=48 --requests=500
```

Production `.env` should include:

- `USE_SQLITE=False`
- `DJANGO_DEBUG=False`
- Strong `DJANGO_SECRET_KEY` and `MEMORIAL_ADMIN_PASSWORD`
- MySQL `DB_*` variables
- Writable `var/cache/` (or custom `CACHE_DIR`)

Optional: Redis cache (`CACHE_BACKEND=django.core.cache.backends.redis.RedisCache`) if your host provides it — best when many Passenger workers hammer the cache at once.

On Windows, local `stress_test` uses in-memory cache automatically (file cache is not safe under extreme parallel writes on NTFS).

## Verify health

- `GET /health/` → `{"status":"ok"}` (DB checked; result cached ~5s)

## After content changes

Dashboard saves invalidate the relevant caches automatically. If you edit data in Django admin or the shell, restart the app or clear `var/cache/` if pages look stale.

## Stress test

```bash
python manage.py stress_test
```

Options: `--workers`, `--requests`, `--max-error-rate`, `--max-p95-ms`.

Fails exit code 1 if error rate or latency thresholds are exceeded.
