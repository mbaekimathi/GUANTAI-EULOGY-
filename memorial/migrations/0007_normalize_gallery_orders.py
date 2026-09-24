from django.db import migrations


def normalize_orders(apps, schema_editor):
    GalleryImage = apps.get_model("memorial", "GalleryImage")
    photos = list(GalleryImage.objects.order_by("order", "id"))
    for index, photo in enumerate(photos):
        if photo.order != index:
            photo.order = index
            photo.save(update_fields=["order"])


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0006_home_visit_mbogori_coords"),
    ]

    operations = [
        migrations.RunPython(normalize_orders, migrations.RunPython.noop),
    ]
