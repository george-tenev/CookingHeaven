from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def is_alpha(value):
    if not value.isalpha():
        raise ValidationError("Enter only alphabetic symbols!")



