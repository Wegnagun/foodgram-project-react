from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser, Follow


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed')
        extra_kwargs = {'is_subscribed': {'required': False}}

    def get_is_subscribed(self, obj: CustomUser):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()

    def to_representation(self, obj):
        """ Возвращаем результаты работы сериализатора."""
        result = super(CustomUserSerializer, self).to_representation(obj)
        result.pop('password', None)
        result.pop('is_superuser', None)
        return result


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed',)
        read_only_fields = ('is_superuser',)


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор пароля."""

    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['current_password', 'new_password']

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError('Неправильный текущий пароль!')
        return value

    def validate(self, data):
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError(
                {'new_password': "Должен отличаться от старого!"}
            )
        validate_password(data['new_password'], self.context['user'])
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['user']
        user.set_password(password)
        user.save()
        return user


class UsersListSerializer(serializers.ModelSerializer):
    """Сериализатор списка пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email", "id", "username", "first_name", "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if (
            request
            and hasattr(request, "user")
            and request.user.is_authenticated
        ):
            return request.user.follower.filter(author=obj).exists()
        return False
