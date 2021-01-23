from django.core.exceptions import ValidationError


def is_phone(value):
    if not value.isdigit() and not len(value) == 11:
        raise ValidationError("Please enter a valid phone number")
