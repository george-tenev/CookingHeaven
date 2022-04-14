from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def is_alpha(value):
    if not all(char.isalpha() for char in value):
        raise ValidationError("Enter only alphabetic symbols!")

def is_alpha_and_space(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Enter only alphabetic symbols and space !")


