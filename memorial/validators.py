from django.core.exceptions import ValidationError

MAX_UPLOAD_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "gif", "webp")


def validate_upload_image_size(upload):
    if upload and getattr(upload, "size", 0) > MAX_UPLOAD_IMAGE_BYTES:
        raise ValidationError(
            "Image must be 10 MB or smaller. Choose a smaller file or compress the photo."
        )
