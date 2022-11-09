from django.contrib import admin

from users.admin import BaseAdminSettings
from .models import Tag


class TagsAdmin(BaseAdminSettings):
    """Отображаемые поля админки раздела тэги."""
    list_display = (
        'name',
        'color',
        'colored',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


admin.site.register(Tag, TagsAdmin)
