from django.core.management.base import BaseCommand

from memorial.content_data import DEFAULT_LIFE_CHAPTERS
from memorial.models import LifeChapter


class Command(BaseCommand):
    help = "Replace life story chapters with Fredrick Guantai Mugira biography content."

    def handle(self, *args, **options):
        LifeChapter.objects.all().delete()
        for year, order, title, body in DEFAULT_LIFE_CHAPTERS:
            LifeChapter.objects.create(
                year=year, title=title, body=body, order=order
            )
        self.stdout.write(
            self.style.SUCCESS(f"Updated {len(DEFAULT_LIFE_CHAPTERS)} life story chapters.")
        )
