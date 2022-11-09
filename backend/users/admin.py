from django.contrib import admin

from .models import User


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = '-пусто-'
    list_filter = ('email', 'username')


class UserAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела пользователи."""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_superuser'
    )
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')


admin.site.register(User, UserAdmin)
