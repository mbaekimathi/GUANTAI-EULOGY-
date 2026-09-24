# Memorial — Fredrick Guantai Mugira

A modern, responsive memorial site with a consistent **header**, **sidebar**, and **footer**. Built with **Django** and **PyMySQL** (MySQL) for production; SQLite is enabled by default for local development.

## Features

- Responsive layout for mobile, tablet, and desktop (collapsible sidebar on small screens)
- Pages: Home, Eulogy, Life Story, Legacy, Family, Tributes (with form), Service
- Django models for timeline chapters, guest tributes, and quotes
- Admin interface for content moderation

## Quick start (local)

```powershell
cd "c:\DEV OPS\WEBSITES\GUANTAI"
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_memorial
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Create a superuser for admin:

```powershell
python manage.py createsuperuser
```

Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## MySQL with PyMySQL

1. Create a database (example: `guantai_memorial`).
2. Copy `.env.example` to `.env`.
3. Set `USE_SQLITE=False` and fill in `DB_*` variables.
4. Run migrations:

```powershell
python manage.py migrate
python manage.py seed_memorial
```

PyMySQL is registered in `config/__init__.py` via `pymysql.install_as_MySQLdb()`.

## cPanel deployment

See **[DEPLOY_CPANEL.md](DEPLOY_CPANEL.md)** for Setup Python App fields, environment variables, and post-deploy commands.

## Customization

- Honoree details: `MEMORIAL` dict in `config/settings.py`
- Copy and photos: edit templates under `templates/memorial/`
- Styles: `static/css/main.css`
