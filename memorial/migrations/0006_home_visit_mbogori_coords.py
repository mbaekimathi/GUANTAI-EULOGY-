from django.db import migrations


def set_home_mbogori_coords(apps, schema_editor):
    VisitLocation = apps.get_model("memorial", "VisitLocation")
    VisitLocation.objects.filter(slug="home").update(
        maps_query="-0.2002388,37.6044681",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0005_church_visit_mbogori_coords"),
    ]

    operations = [
        migrations.RunPython(set_home_mbogori_coords, migrations.RunPython.noop),
    ]
