from django.db import migrations

PROGRAMME_LEAD = (
    "Burial and homegoing service — Friday, 25 September 2026 at "
    "PCEA Mbogori Church, Chogoria (Mbogori Marigwe)."
)
PROGRAMME_TIMELINE = """Friday, 25 September 2026 : Burial day
7:00 AM : Departure from home – Mbogori
8:00 AM : Arrival at mortuary — viewing of the body
9:00 AM : Departure from Chogoria
10:00 AM : Arrival at PCEA Mbogori Church, Chogoria
10:30 AM : Funeral service and burial"""


def apply_friday_burial_date(apps, schema_editor):
    HomePageContent = apps.get_model("memorial", "HomePageContent")
    row = HomePageContent.objects.first()
    if row:
        row.programme_lead = PROGRAMME_LEAD
        row.programme_timeline = PROGRAMME_TIMELINE
        row.save(update_fields=["programme_lead", "programme_timeline", "updated_at"])


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0010_tribute_list_index"),
    ]

    operations = [
        migrations.RunPython(apply_friday_burial_date, migrations.RunPython.noop),
    ]
