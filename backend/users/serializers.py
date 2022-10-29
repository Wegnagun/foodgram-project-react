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


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_superuser', 'is_blocked',)  # 'is_subscribed'
        read_only_fields = ('is_superuser', 'is_blocked',)


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор пароля."""

    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

