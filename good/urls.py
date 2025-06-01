from django.urls import path

from . import views

urlpatterns = [
    path('<slug:city_slug>/', views.product, name='catalog'),

    # Важно: более специфичные маршруты должны быть выше!
    # Сначала проверяем товары (у них 3 сегмента)
    path('<slug:city_slug>/<slug:category_slug>/<slug:product_slug>/',
         views.show_product, name='product'),

    # Затем проверяем категории и теги (у них 2 сегмента)
    path('<slug:city_slug>/<slug:slug>/',
         views.show_category_or_tag, name='category_or_tag'),

    # Оставляем старый маршрут для обратной совместимости
    path('<slug:city_slug>/<slug:category_slug>/',
         views.show_category, name='category'),
]
