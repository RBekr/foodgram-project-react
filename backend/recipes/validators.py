from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    message = 'Время приготовления в минутах не может быть меньше 1'
    if value < 1:
        raise ValidationError(
            message,
            params={'value': value},
        )
    return value


def measurement_unit_is_character(value):
    message = 'Единица измерения может принимать только буквенные символы {}'
    if not value.isalpha():
        raise ValidationError(
            message.format(value)
        )
    return value
