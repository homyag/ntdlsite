from django.contrib import admin

from good.models import Category, Product, City, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'sort_order', 'products_count', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('sort_order', 'is_active')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'sort_order', 'is_active')
        }),
        ('Описания', {
            'fields': ('description', 'catalog_title', 'catalog_description')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Количество товаров'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'parent', 'products_count')
    list_filter = ('parent',)
    search_fields = ('name', 'description')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Дополнительно', {
            'fields': ('small_text_for_catalog',)
        })
    )

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city', 'price', 'category', 'get_tags', 'on_stock')
    list_filter = ['city', 'category', 'price', 'tags', 'on_stock']
    list_editable = ('price', 'on_stock')
    filter_horizontal = ('tags',)  # Удобный виджет для выбора тегов
    search_fields = ('name', 'description')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'city', 'category', 'price', 'on_stock')
        }),
        ('Описания', {
            'fields': ('description', 'product_card_description', 'product_card_property')
        }),
        ('Теги', {
            'fields': ('tags',)
        }),
        ('Изображение', {
            'fields': ('img',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)