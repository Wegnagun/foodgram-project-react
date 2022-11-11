from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        extra_kwargs = {'is_subscribed': {'required': False}}

    def get_is_subscribed(self, obj: User):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return request.user.subscribe.filter(subscribe=obj).exists()
        return False
