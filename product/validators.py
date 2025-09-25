from django.core.exceptions import ValidationError


def validate_file_size(file):
    """this validator validate if file size is less than  10MB"""

    max_size=10
    max_size_in_bytes=max_size * 1024*1024

    if file.size> max_size_in_bytes:
        raise ValidationError(f"File can not be lagrer than{max_size} MB")