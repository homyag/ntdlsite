from django.contrib.sitemaps import Sitemap as DjangoSitemap


class BaseSitemap(DjangoSitemap):
    """Базовый класс для всех sitemap с поддержкой изображений"""

    def get_urls(self, page=1, site=None, protocol=None):
        """Переопределяем метод get_urls, чтобы явно добавлять изображения к URL"""
        # Вызываем оригинальный метод
        urls = super().get_urls(page, site, protocol or self.protocol)

        # Добавляем изображения, если есть соответствующий метод
        for url in urls:
            item = url.get('item', None)
            if item and hasattr(self, 'get_images'):
                try:
                    images = self.get_images(item)
                    if images:
                        url['images'] = images
                except Exception as e:
                    print(f"Ошибка при получении изображений для {item}: {e}")

        return urls