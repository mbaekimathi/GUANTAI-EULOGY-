from django.core.management.base import BaseCommand

from memorial.content_data import (
    DEFAULT_HOME_PAGE,
    seed_default_life_chapters,
    sync_default_tributes,
)
from memorial.models import HomePageContent, MemorialQuote


class Command(BaseCommand):
    help = "Seed life chapters, quotes, and sample tributes for Fredrick Guantai Mugira."

    def handle(self, *args, **options):
        created = seed_default_life_chapters()
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created {created} life chapters."))
        else:
            self.stdout.write("Life chapters already exist — skipping chapter seed.")

        if not HomePageContent.objects.exists():
            HomePageContent.objects.create(**DEFAULT_HOME_PAGE)
            self.stdout.write(self.style.SUCCESS("Created home page content and programme."))

        if not MemorialQuote.objects.filter(is_active=True).exists():
            MemorialQuote.objects.create(
                text="Those who live in hearts we leave behind do not die.",
                attribution="Thomas Campbell",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS("Created featured quote."))

        created_tributes = sync_default_tributes()
        if created_tributes:
            self.stdout.write(self.style.SUCCESS(f"Created {created_tributes} tributes."))
        else:
            self.stdout.write("Tributes already exist — skipping tribute seed.")

        self.stdout.write(self.style.SUCCESS("Memorial seed complete."))
