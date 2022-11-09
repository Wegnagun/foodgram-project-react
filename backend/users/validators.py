from django.core.exceptions import ValidationError


def validate_not_me_name(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать никнейм "me" запрещено.'
        )
