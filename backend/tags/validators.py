from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class HexColorValidator(validators.RegexValidator):
    regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    message = ("Недопустимый вид Hex тега")
    flag = 0
