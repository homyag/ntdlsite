from django.urls import path

from . import views

urlpatterns = [
    path('', views.product, name='catalog'),
    path('<slug:category_slug>/', views.show_category,
         name='category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.show_product,
         name='product'),
]
