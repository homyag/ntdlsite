from django.db import models
from django.db.models import SlugField
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(on_stock=True)


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("city", kwargs={"city_slug": self.slug})


