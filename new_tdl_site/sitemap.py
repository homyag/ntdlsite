import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from good.models import Product, Category


# Static Sitemap
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['home', 'about', 'contacts', 'services', 'delivery']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return datetime.datetime.now()

    def image(self, item):
        images = {
            'home': 'static/images/logo/logo.svg',
        }
        return [images[item]] if item in images else []


#Products sitemap
class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Product.published.all()  # Выводим только товары в наличии

    def lastmod(self, obj):
        return obj.time_update

    def location(self, obj):
        return obj.get_absolute_url()

    def image(self, obj):
        if obj.img:
            return [obj.img.url]  # Возвращаем URL изображения товара
        return []


# Products category sitemap

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        if obj.products.exists():
            return obj.products.latest('time_update').time_update
        return None
