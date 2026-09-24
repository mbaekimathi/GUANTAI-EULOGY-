from django.db import migrations


def set_church_mbogori_coords(apps, schema_editor):
    VisitLocation = apps.get_model("memorial", "VisitLocation")
    VisitLocation.objects.filter(slug="church").update(
        place_name="PCEA Mbogori church — Mbogori Marigwe",
        maps_query="-0.2002388,37.6044681",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0004_homepagecontent_portrait_image"),
    ]

    operations = [
        migrations.RunPython(set_church_mbogori_coords, migrations.RunPython.noop),
    ]
