# Deploy on cPanel (Setup Python App)

## Python app form

| Field | Value |
|--------|--------|
| **Application root** | `GUANTAI` (folder containing `manage.py`) |
| **Application URL** | Your domain (e.g. `guantai.projectlucas.co.ke`) |
| **Application startup file** | `passenger_wsgi.py` |
| **Application entry point** | `application` |

## Environment variables (cPanel → Add variable)

Set these in **Setup Python App** (or copy `.env.example` to `.env` on the server — not in git):

```
DJANGO_SECRET_KEY=<long random string>
DJANGO_DEBUG=False
ALLOWED_HOSTS=guantai.projectlucas.co.ke
CSRF_TRUSTED_ORIGINS=https://guantai.projectlucas.co.ke
USE_SQLITE=False
DB_NAME=<cpanel_mysql_database>
DB_USER=<cpanel_mysql_user>
DB_PASSWORD=<mysql_password>
DB_HOST=localhost
DB_PORT=3306
MEMORIAL_ADMIN_USERNAME=<your choice>
MEMORIAL_ADMIN_PASSWORD=<strong password>
```

Create the MySQL database and user in cPanel **MySQL® Databases**, then grant the user access to the database.

## After creating the app

Open **Setup Python App** → your app → **Enter to virtual environment** (or SSH), then from the application root:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_memorial
python manage.py createsuperuser
```

Ensure the `media/` directory exists and is writable (uploads for gallery and homepage portrait):

```bash
mkdir -p media
chmod 755 media
```

Restart the Python application from cPanel after env changes or code updates.

Full performance notes: **[docs/PERFORMANCE.md](docs/PERFORMANCE.md)**.

## High traffic (many visitors at once)

Before a funeral livestream or announcement that will drive heavy traffic:

1. **Use MySQL**, not SQLite: `USE_SQLITE=False` with the `DB_*` variables above. SQLite cannot handle many simultaneous writes.
2. Run **`python manage.py seed_memorial`** and **`python manage.py migrate`** so the site does not seed content on first visitor hits.
3. Run **`python manage.py collectstatic --noinput`** so WhiteNoise serves compressed assets (not Django per request).
4. Ensure **`var/cache/`** (or your `CACHE_DIR`) is writable — sessions use `cached_db` and public pages share a file cache across workers.
5. Optional: point **`CACHE_BACKEND=django.core.cache.backends.redis.RedisCache`** and set Redis `LOCATION` if your host provides Redis (best for many Passenger workers).
6. Monitor **`/health/`** — returns `{"status":"ok"}` when the app and database respond.
7. After deploy, run **`python manage.py stress_test`** from the app venv (optional `--workers=48 --requests=500`) to verify error rate and latency before a live event.

Run **`python manage.py check --deploy`** before go-live; resolve warnings about secret key, admin password, and SQLite.

## Deploy updates from GitHub

```bash
cd ~/GUANTAI   # or your application root path
git pull
source /home/USERNAME/virtualenv/GUANTAI/3.13/bin/activate   # path shown in cPanel
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then restart the app in cPanel.

## Troubleshooting

- **500 error**: Check **Errors** in cPanel or `stderr.log` in the app folder; confirm `DJANGO_DEBUG=False` and env vars are set.
- **Static files missing**: Run `collectstatic` and restart the app (WhiteNoise serves from `staticfiles/`).
- **CSRF / login failures on HTTPS**: Add your full site URL to `CSRF_TRUSTED_ORIGINS` with `https://`.
