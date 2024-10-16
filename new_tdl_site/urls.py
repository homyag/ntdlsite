from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from new_tdl_site.views import page_not_found

from .sitemap import StaticViewSitemap, ProductSitemap, CategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
}


admin.site.site_header = "Торговый Дом Ленинградский - административная панель"

admin.site.site_title = "Торговый Дом Ленинградский"

urlpatterns = [
    path('tdladmin/', admin.site.urls),
    path('catalog/', include('good.urls')),
    path('', include('commonpages.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemap_with_images.xml'}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

handler404 = page_not_found


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)