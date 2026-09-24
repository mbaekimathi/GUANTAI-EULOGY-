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
