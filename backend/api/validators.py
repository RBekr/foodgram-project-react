import re
from rest_framework import serializers

def username_not_me(value):
    message = 'Имя пользователя не может быть равно {}'
    if re.match(r'(?i)me', value) or value == '':
        raise serializers.ValidationError(
            message.format(value)
        )
    return value