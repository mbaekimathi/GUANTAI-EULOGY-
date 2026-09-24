from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0008_burial_date_sept_2026"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryimage",
            name="thumbnail",
            field=models.ImageField(blank=True, upload_to="gallery/thumbnails/"),
        ),
    ]
