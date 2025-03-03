from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from new_tdl_site.views import page_not_found

from leads.views import (CallsApiList, \
                         CallsApiUpdate, CallsByManagerTgIdApiList,
                         CallsByManagerTgIdApiUpdate,
                         CallByManagerTgIdAndDateRangeApiList,
                         CallCommentUpdateView, ManagersApiList,
                         CallsDetailView, CallResultUpdateView, ResultsApiList,
                         CallManagerUpdateView)

from .sitemap import StaticViewSitemap, ProductSitemap, CategorySitemap, \
    CatalogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'catalogs': CatalogSitemap,
}


admin.site.site_header = "Торговый Дом Ленинградский - административная панель"

admin.site.site_title = "Торговый Дом Ленинградский"

urlpatterns = [
    path('tdladmin/', admin.site.urls),
    path('api/v1/callslist/', CallsApiList.as_view()), # получает весь
    # список заявок по GET запросу и добавляет новую заявку по POST запросу
    path('api/v1/managers/', ManagersApiList.as_view()), # получает весь
    # список менеджеров по GET запросу и добавляет нового менеджера по POST
    # запросу
    path('api/v1/results/', ResultsApiList.as_view()), # получает весь
    # список результатов по GET запросу и добавляет новые резудьтаты по POST
    path('api/v1/callslist/<int:pk>/', CallsApiUpdate.as_view()),
    # обновляет одну заявку
    path('api/v1/callslist/call/<int:pk>/', CallsDetailView.as_view()),
    # получает одну заявку по id заявки
    path('api/v1/callslist/manager-tg/<int:tg_id>/',
         CallsByManagerTgIdApiList.as_view()), # получает список заявок по
    # telegram id менеджера
    path('api/v1/callslist/manager-tg/<int:tg_id>/<int:pk>/',
         CallsByManagerTgIdApiUpdate.as_view()), # обновляет заявку по id менеджера и id заявки
    path('api/v1/callslist/filter/',
         CallByManagerTgIdAndDateRangeApiList.as_view()),
    path('api/v1/callslist/comment_update/<int:pk>/',
         CallCommentUpdateView.as_view()), # обновляет комментарий
    path('api/v1/callslist/result_update/<int:pk>/',
         CallResultUpdateView.as_view()), # обновляет статус заявки
    path('api/v1/callslist/manager_update/<int:pk>/',
         CallManagerUpdateView.as_view()), # обновляет менеджера в заявке
    path('catalog/', include('good.urls')),
    path('', include('commonpages.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemap_with_images.xml'}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('1qc4a638hqkvzjrs1rss11hhgqxdqvt5.txt', TemplateView.as_view(
        template_name='1qc4a638hqkvzjrs1rss11hhgqxdqvt5.txt',
        content_type='text/plain')),
]

handler404 = page_not_found


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)