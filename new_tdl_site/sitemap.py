import datetime
from django.utils import timezone
from django.urls import reverse

from good.models import Product, Category, City
from blog.models import Post, Category as BlogCategory, Tag

from .base_sitemap import BaseSitemap  # Импортируем наш новый базовый класс


# Static Sitemap
class StaticViewSitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    priority = 0.8
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['home',
                'about',
                'contacts',
                'services',
                'delivery',
                'concrete_calculator',
                ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

    def get_images(self, item):
        images = {
            'home': '/static/images/logo/logo.svg',
        }
        if item in images:
            return [{'loc': images[item]}]
        return []


# Products sitemap
class ProductSitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'daily'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.time_update

    def location(self, obj):
        return obj.get_absolute_url()

    def get_images(self, obj):
        if obj.img:
            return [{'loc': obj.img.url}]
        return []


# Products category sitemap
class CategorySitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        items = []
        cities = City.objects.all()
        categories = Category.objects.all()
        for city in cities:
            for category in categories:
                if Product.objects.filter(city=city,
                                          category=category).exists():
                    items.append((city, category))
        return items

    def location(self, obj):
        city, category = obj
        return reverse("category", kwargs={
            "city_slug": city.slug,
            "category_slug": category.slug
        })

    def lastmod(self, obj):
        city, category = obj
        products = Product.objects.filter(city=city, category=category)
        if products.exists():
            return products.latest('time_update').time_update
        return timezone.now()

    def get_images(self, obj):
        city, category = obj
        product = Product.objects.filter(city=city, category=category).first()
        if product and product.img:
            return [{'loc': product.img.url}]
        return []


# Catalog Sitemap
class CatalogSitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return City.objects.all().order_by('id')

    def location(self, obj):
        return reverse("catalog", kwargs={"city_slug": obj.slug})

    def lastmod(self, obj):
        latest_product = Product.published.filter(city=obj).order_by('-time_update').first()
        if latest_product:
            return latest_product.time_update
        return timezone.now()

    def get_images(self, obj):  # Переименовано с images на get_images
        product = Product.objects.filter(city=obj).first()
        if product and product.img:
            return [{'loc': product.img.url}]
        return [{'loc': '/static/images/logo/logo.svg'}]


class BlogPostSitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return obj.get_absolute_url()

    def get_images(self, obj):  # Переименовано с images на get_images
        if obj.image:
            return [{'loc': obj.image.url}]
        return []


# Добавляем класс для категорий блога
class BlogCategorySitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return BlogCategory.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        posts = Post.objects.filter(category=obj, is_published=True).order_by('-updated_date')
        if posts.exists():
            return posts.first().updated_date
        return timezone.now()

    def get_images(self, obj):  # Переименовано с images на get_images
        post = Post.objects.filter(category=obj, is_published=True).first()
        if post and post.image:
            return [{'loc': post.image.url}]
        return []


# Добавляем класс для тегов блога
class BlogTagSitemap(BaseSitemap):  # Используем BaseSitemap вместо Sitemap
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        posts = Post.objects.filter(tags=obj, is_published=True).order_by('-updated_date')
        if posts.exists():
            return posts.first().updated_date
        return timezone.now()

    def get_images(self, obj):  # Переименовано с images на get_images
        post = Post.objects.filter(tags=obj, is_published=True).first()
        if post and post.image:
            return [{'loc': post.image.url}]
        return []