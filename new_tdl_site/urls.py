from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from new_tdl_site.views import page_not_found


admin.site.site_header = "Торговый Дом Ленинградский - административная панель"

admin.site.site_title = "Торговый Дом Ленинградский"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('good.urls')),
    path('', include('commonpages.urls')),
    path('', include('blog.urls')),
]

handler404 = page_not_found


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)