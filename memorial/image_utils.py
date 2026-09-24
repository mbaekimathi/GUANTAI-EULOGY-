from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def build_gallery_thumbnail(image_field, *, max_side=960, quality=82):
    """
    Smaller JPEG for grid / preview (full image kept for lightbox).
    Returns ContentFile or None if processing fails.
    """
    if not image_field:
        return None
    try:
        with image_field.open("rb") as handle:
            img = Image.open(handle)
            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
            buffer.seek(0)
            return ContentFile(buffer.read())
    except OSError:
        return None
