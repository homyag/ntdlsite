from django.contrib import admin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'is_published', 'views')
    list_filter = ('is_published', 'category', 'tags', 'pub_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'pub_date'
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Категоризация', {
            'fields': ('category', 'tags')
        }),
        ('Публикация', {
            'fields': ('is_published', 'views')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )