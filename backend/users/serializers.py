from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'is_superuser', 'is_blocked')
        read_only_fields = ('is_superuser', 'is_blocked',)

