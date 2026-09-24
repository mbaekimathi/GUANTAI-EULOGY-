from django.core.management.base import BaseCommand

from memorial.image_utils import build_gallery_thumbnail
from memorial.models import GalleryImage


class Command(BaseCommand):
    help = "Build grid thumbnails for gallery photos (faster page loads)."

    def handle(self, *args, **options):
        count = 0
        for photo in GalleryImage.objects.order_by("order", "id"):
            if not photo.image:
                continue
            thumb_content = build_gallery_thumbnail(photo.image)
            if not thumb_content:
                self.stderr.write(f"Skipped photo {photo.pk} (could not process image).")
                continue
            if photo.thumbnail:
                photo.thumbnail.delete(save=False)
            photo.thumbnail.save(f"{photo.pk}_grid.jpg", thumb_content, save=True)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Generated {count} gallery thumbnail(s)."))
