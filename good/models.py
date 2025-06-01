from django.db import models
from django.db.models import SlugField
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(on_stock=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тега")
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL"
    )
    description = models.TextField(blank=True, verbose_name="Описание тега")

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    # Дополнительные поля для каталожных страниц
    catalog_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок на странице каталога"
    )
    catalog_description = models.TextField(
        blank=True,
        verbose_name="Описание на странице каталога"
    )

    # Поля для группировки и сортировки
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Категория тега",
        help_text="Например: применение, марка, тип"
    )
    sort_order = models.IntegerField(default=0, verbose_name="Порядок сортировки")

    # Активность тега
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['slug'], name='good_tag_slug_idx'),
            models.Index(fields=['category'], name='good_tag_category_idx'),
            models.Index(fields=['is_active'], name='good_tag_active_idx'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url_for_city(self, city_slug):
        """Получение URL для конкретного города"""
        return reverse("category_or_tag", kwargs={
            "city_slug": city_slug,
            "slug": self.slug
        })


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug: SlugField = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL",
        db_index=True,
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    product_card_description = models.TextField(
        blank=True, verbose_name="Описание в карточке"
    )
    product_card_property = models.TextField(
        blank=True, verbose_name="Свойства в карточке"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    on_stock = models.BooleanField(default=True, verbose_name="В наличии")
    img = models.ImageField(
        upload_to="good/goods_images", blank=True, null=True,
        verbose_name="Изображение"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products",
    )
    city = models.ForeignKey(
        "City",
        on_delete=models.CASCADE,
        verbose_name="Город",
        related_name="products",
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='products',
        verbose_name="Теги"
    )

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()

    class Meta:
        ordering = ['-time_create']
        db_table: str = "good"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=['city', 'category', 'on_stock'], name='good_city_cat_stock_idx'),
            models.Index(fields=['slug'], name='good_slug_idx'),
            models.Index(fields=['name'], name='good_name_idx'),  # Для поиска по имени
            models.Index(fields=['price'], name='good_price_idx'),  # Для сортировки по цене
            models.Index(fields=['time_create'], name='good_time_create_idx'),  # Для сортировки по времени создания
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.city is None or self.city.slug is None:
            raise ValueError(f"Product {self.id} {self.name} has no city or "
                             f"city slug.")
        if self.category is None or self.category.slug is None:
            raise ValueError(
                f"Product {self.id} {self.name} has no category or category "
                f"slug.")

        return reverse(
            "product",
            kwargs={
                "city_slug": self.city.slug,
                "category_slug": self.category.slug,
                "product_slug": self.slug,
            },
        )


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug: SlugField = models.SlugField(
        max_length=255, unique=True, blank=True, null=True, verbose_name="URL"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Родительская категория",
    )
    description = models.TextField(blank=True, verbose_name="Описание категории")
    small_text_for_catalog = models.TextField(
        blank=True, verbose_name="Короткое описание под title каталога"
    )

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=['parent'], name='good_cat_parent_idx'),
            models.Index(fields=['slug'], name='good_cat_slug_idx'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название города")
    slug: SlugField = models.SlugField(
        max_length=255, unique=True, blank=True, null=True, verbose_name="URL"
    )
    region = models.CharField(max_length=255, verbose_name="Регион",
                              blank=True, null=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        indexes = [
            models.Index(fields=['slug'], name='good_city_slug_idx'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("city", kwargs={"city_slug": self.slug})
