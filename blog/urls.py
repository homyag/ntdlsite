from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('blog/tag/<slug:tag_slug>/', views.blog_tag, name='blog_tag'),
    path('blog/<slug:post_slug>/', views.blog_post, name='blog_post'),
]