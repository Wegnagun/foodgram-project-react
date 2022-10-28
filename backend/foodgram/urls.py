from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Разделы админки Foodgram'
admin.site.site_title = 'Админка сайта Foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
