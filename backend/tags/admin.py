from django.contrib import admin

from users.admin import BaseAdminSettings
from .models import Tag
from django.utils.html import format_html


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

    @admin.display
    def colored(self, obj):
        return format_html(
            f'<span style="background: {obj.color};'
            f'color: {obj.color}";>___________</span>'
        )
    colored.short_description = 'цвет'


admin.site.register(Tag, TagsAdmin)
