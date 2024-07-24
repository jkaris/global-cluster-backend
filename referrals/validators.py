from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size = 10 * 1024 * 1024  # 10 MB
    if image.size > max_size:
        raise ValidationError(f"Image file too large ( > {max_size} bytes )")
