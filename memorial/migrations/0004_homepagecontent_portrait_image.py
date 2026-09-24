from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memorial", "0003_homepagecontent"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepagecontent",
            name="portrait_image",
            field=models.ImageField(
                blank=True,
                help_text="Photo shown in the hero portrait on the public home page.",
                upload_to="home/portraits/",
            ),
        ),
    ]
