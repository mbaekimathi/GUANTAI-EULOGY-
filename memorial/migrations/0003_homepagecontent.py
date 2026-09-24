from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0002_eulogycontent_galleryimage_visitlocation"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("intro_lead", models.TextField()),
                ("portrait_caption", models.CharField(max_length=300)),
                ("programme_title", models.CharField(max_length=200)),
                ("programme_lead", models.TextField(blank=True)),
                (
                    "programme_timeline",
                    models.TextField(
                        help_text="One event per line, e.g. 7:00 AM : Departure from home",
                    ),
                ),
                (
                    "programme_service",
                    models.TextField(
                        help_text="Order of service — one item per line.",
                    ),
                ),
                ("programme_closing", models.CharField(blank=True, max_length=300)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Home page content",
            },
        ),
    ]
