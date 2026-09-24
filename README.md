# Memorial — Fredrick Guantai Mugira

A modern, responsive memorial site with a consistent **header**, **sidebar**, and **footer**. Built with **Django** and **PyMySQL** (MySQL) for production; SQLite is enabled by default for local development.

## Features

- Responsive layout for mobile, tablet, and desktop (collapsible sidebar on small screens)
- Pages: Home, Life Story, Legacy, Family, Tributes, Gallery, Visit, Service
- Family **dashboard** for content updates (home, life story, tributes, gallery, locations)
- Django admin for advanced moderation
- **Optimized for concurrent visitors** — caching, compressed static files, stress-test command

## Quick start (local)

```powershell
cd "c:\DEV OPS\WEBSITES\GUANTAI"
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_memorial
python manage.py collectstatic --noinput
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Dashboard login: [http://127.0.0.1:8000/dashboard/login/](http://127.0.0.1:8000/dashboard/login/) (credentials via `.env` — see `.env.example`)

Django admin (optional):

```powershell
python manage.py createsuperuser
```

Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## MySQL with PyMySQL (production)

1. Create a database (example: `guantai_memorial`).
2. Copy `.env.example` to `.env`.
3. Set `USE_SQLITE=False` and fill in `DB_*` variables.
4. Run migrations and seed:

```powershell
python manage.py migrate
python manage.py seed_memorial
python manage.py collectstatic --noinput
```

PyMySQL is registered in `config/__init__.py` via `pymysql.install_as_MySQLdb()`.

## Performance & load testing

See **[docs/PERFORMANCE.md](docs/PERFORMANCE.md)** for the full checklist.

Quick verification:

```powershell
python manage.py test memorial
python manage.py stress_test --workers=48 --requests=500
```

Health endpoint: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

## cPanel deployment

See **[DEPLOY_CPANEL.md](DEPLOY_CPANEL.md)** for Setup Python App fields, environment variables, and post-deploy commands.

## Customization

- Honoree details: `MEMORIAL` dict in `config/settings.py`
- Copy and photos: dashboard or templates under `templates/memorial/`
- Styles: `static/css/main.css`
