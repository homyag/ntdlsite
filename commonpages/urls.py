from django.urls import path

from . import views

menu = ["О компании", "Контакты", "Продукция", "Блог", "Услуги"]

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("services/", views.services, name="services"),
    path("services/delivery", views.delivery, name="delivery"),
    path('submit_callback/', views.submit_callback, name='submit_callback'),
    path('set_city/', views.set_city, name='set_city'),
    path('change_city/', views.change_city, name='change_city'),
]
