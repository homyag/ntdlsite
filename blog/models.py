from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import strip_tags
from tinymce.models import HTMLField
import re


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_tag', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL статьи")
    content = HTMLField(verbose_name="Контент статьи")
    excerpt = models.TextField(blank=True, verbose_name="Краткое саммари в карточке")
    image = models.ImageField(upload_to='blog/images/%Y/%m/', blank=True, verbose_name="Изображение")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts',
                                 verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Теги")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    # SEO поля
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name="Meta Keywords")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.excerpt and self.content:
            # Извлекаем первые 200 символов текста без HTML тегов
            plain_text = strip_tags(self.content)
            # Удаляем множественные пробелы
            plain_text = re.sub(r'\s+', ' ', plain_text).strip()
            self.excerpt = plain_text[:200] + '...' if len(plain_text) > 200 else plain_text

        super().save(*args, **kwargs)