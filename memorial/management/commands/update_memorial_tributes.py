from django.core.management.base import BaseCommand

from memorial.content_data import sync_default_tributes


class Command(BaseCommand):
    help = "Replace memorial tributes with the family's default tribute messages."

    def handle(self, *args, **options):
        count = sync_default_tributes(replace=True)
        self.stdout.write(self.style.SUCCESS(f"Updated {count} tributes."))
