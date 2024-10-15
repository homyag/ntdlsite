from django.contrib import admin

from good.models import Category, Product, City


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city', 'category')
    list_filter = ['city', 'category']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)