from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_superuser', 'is_blocked',)  # 'is_subscribed'
        read_only_fields = ('is_superuser', 'is_blocked',)
        # extra_kwargs = {'is_subscribed': {'required': False}}

    def to_representation(self, obj):
        """ Возвращаем результаты работы сериализатора."""
        result = super(CustomUserSerializer, self).to_representation(obj)
        result.pop('password', None)
        return result

