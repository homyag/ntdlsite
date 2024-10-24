from django.urls import path

from . import views


urlpatterns = [
    path('<slug:city_slug>/', views.product, name='catalog'),
    path('<slug:city_slug>/<slug:category_slug>/', views.show_category,
         name='category'),
    path('<slug:city_slug>/<slug:category_slug>/<slug:product_slug>/',
         views.show_product, name='product'),
]
