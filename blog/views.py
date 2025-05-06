from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse

from .models import Post, Category, Tag
from good.models import Product, Category as ProductCategory, City

# Количество статей на странице
POSTS_PER_PAGE = 6


class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog_main.html'
    context_object_name = 'posts'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)

        # Фильтрация по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None

        # Фильтрация по тегу
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.tag)
        else:
            self.tag = None

        # Поиск
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )

        # Сортировка
        sort = self.request.GET.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.order_by('-views')
        else:  # По умолчанию - по дате (новые)
            queryset = queryset.order_by('-pub_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем все категории
        context['categories'] = Category.objects.all()

        # Добавляем текущую категорию, если она есть
        if hasattr(self, 'category') and self.category:
            context['category'] = self.category

        # Добавляем текущий тег, если он есть
        if hasattr(self, 'tag') and self.tag:
            context['tag'] = self.tag

        # Добавляем популярные статьи для сайдбара
        context['popular_posts'] = Post.objects.filter(is_published=True).order_by('-views')[:5]

        # Добавляем все теги
        context['tags'] = Tag.objects.all()

        # Добавляем текущий параметр сортировки
        context['current_sort'] = self.request.GET.get('sort', 'latest')

        # Добавляем параметр поиска
        context['search_query'] = self.request.GET.get('q', '')

        # Настройка SEO
        if hasattr(self, 'category') and self.category:
            context['title'] = f'Блог ТД Ленинградский - {self.category.name}'
            context['seo_title'] = f'Статьи в категории {self.category.name} | Блог ТД Ленинградский'
            context[
                'seo_description'] = self.category.description or f'Читайте полезные статьи в категории {self.category.name} в блоге ТД Ленинградский'
        elif hasattr(self, 'tag') and self.tag:
            context['title'] = f'Статьи с тегом {self.tag.name} | Блог ТД Ленинградский'
            context['seo_title'] = f'Статьи с тегом {self.tag.name} | Блог ТД Ленинградский'
            context['seo_description'] = f'Читайте полезные статьи с тегом {self.tag.name} в блоге ТД Ленинградский'
        else:
            context['title'] = 'Блог ТД Ленинградский'
            context['seo_title'] = 'Блог ТД Ленинградский — Статьи о бетоне и строительстве'
            context[
                'seo_description'] = 'Полезные материалы о бетоне, строительстве и тонкостях работы с бетонными смесями от экспертов ТД Ленинградский'

        # Формируем хлебные крошки для блога
        breadcrumbs = [
            {'title': 'Главная', 'url': reverse('home')},
            {'title': 'Блог', 'url': reverse('blog')},
        ]

        if hasattr(self, 'category') and self.category:
            breadcrumbs.append({
                'title': self.category.name,
                'url': reverse('blog_category', kwargs={'category_slug': self.category.slug}),
            })
        elif hasattr(self, 'tag') and self.tag:
            breadcrumbs.append({
                'title': f'Тег: {self.tag.name}',
                'url': reverse('blog_tag', kwargs={'tag_slug': self.tag.slug}),
            })

        context['breadcrumbs'] = breadcrumbs

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        # Получаем объект статьи
        obj = super().get_object(queryset)

        # Увеличиваем счетчик просмотров
        if self.request.session.get(f'viewed_post_{obj.id}') != True:
            obj.views += 1
            obj.save(update_fields=['views'])
            self.request.session[f'viewed_post_{obj.id}'] = True

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        # Добавляем все категории
        context['categories'] = Category.objects.all()

        # Добавляем популярные статьи для сайдбара
        context['popular_posts'] = Post.objects.filter(is_published=True).exclude(id=post.id).order_by('-views')[:5]

        # Добавляем похожие статьи
        if post.category:
            context['related_posts'] = Post.objects.filter(
                category=post.category,
                is_published=True
            ).exclude(id=post.id).order_by('-pub_date')[:3]
        else:
            context['related_posts'] = Post.objects.filter(
                is_published=True
            ).exclude(id=post.id).order_by('-pub_date')[:3]

        # Словарь соответствия категорий блога и категорий товаров
        blog_to_product_categories = {
            'бетон': ['beton'],
            'нерудные материалы': ['nerudnye', 'pesok', 'sheben', 'otsev'],
            'плодородный грунт': ['grunt'],
            'асфальт': ['asfalt']
        }

        product_category_slugs = []

        if post.category:
            category_name = post.category.name.lower()

            # Находим соответствующие категории товаров
            for blog_cat, prod_cats in blog_to_product_categories.items():
                if blog_cat.lower() in category_name:
                    product_category_slugs.extend(prod_cats)
                    break

            # Если не нашли прямого соответствия, пробуем найти по ключевым словам в названии
            if not product_category_slugs:
                for key_word, prod_cats in {
                    'бетон': ['beton'],
                    'щебень': ['sheben'],
                    'песок': ['pesok'],
                    'грунт': ['grunt'],
                    'асфальт': ['asfalt'],
                    'отсев': ['otsev']
                }.items():
                    if key_word in category_name or key_word in post.title.lower():
                        product_category_slugs.extend(prod_cats)

        related_products = []

        # Получаем текущий город из контекста
        current_city_slug = self.request.session.get('city_slug')

        # Если найдены категории товаров
        if product_category_slugs:
            # Получаем объекты категорий товаров
            product_categories = ProductCategory.objects.filter(slug__in=product_category_slugs)

            # Если выбран конкретный город
            if current_city_slug:
                current_city = City.objects.filter(slug=current_city_slug).first()

                if current_city:
                    # Для выбранного города берем товары из каждой подходящей категории
                    for product_cat in product_categories:
                        # Берем все товары из категории для города
                        products = Product.objects.filter(
                            city=current_city,
                            category=product_cat,
                            on_stock=True
                        )[:3]  # Берем максимум 3 товара из каждой категории

                        for product in products:
                            related_products.append(product)

                            # Если набрали 4 товара, останавливаемся
                            if len(related_products) >= 3:
                                break

                        # Если набрали 4 товара, останавливаемся
                        if len(related_products) >= 3:
                            break

            # Если город не выбран, показываем разные товары из разных городов
            else:
                cities = City.objects.all()

                # Для отслеживания названий товаров, чтобы не дублировались
                seen_product_names = set()

                # Для каждого города берем по 1 товару из каждой категории с уникальным названием
                for city in cities:
                    for product_cat in product_categories:
                        # Берем все товары из категории для города
                        products = Product.objects.filter(
                            city=city,
                            category=product_cat,
                            on_stock=True
                        )

                        # Ищем товар с уникальным названием
                        for product in products:
                            # Пропускаем товары с уже добавленными названиями
                            if product.name.lower() in seen_product_names:
                                continue

                            related_products.append(product)
                            seen_product_names.add(product.name.lower())

                            # Если набрали 4 товара, останавливаемся
                            if len(related_products) >= 3:
                                break

                        # Если набрали 4 товара, останавливаемся
                        if len(related_products) >= 3:
                            break

                    # Если набрали 4 товара, останавливаемся
                    if len(related_products) >= 3:
                        break

        # Добавляем связанные товары в контекст
        context['related_products'] = related_products

        # Создаем тематический заголовок для секции товаров
        products_section_title = "Материалы высокого качества"

        if post.category:
            category_name = post.category.name.lower()

            # Формируем заголовок в зависимости от категории статьи
            if 'бетон' in category_name:
                products_section_title = "Бетонные смеси для вашего строительства"
            elif 'нерудн' in category_name:
                products_section_title = "Нерудные материалы высокого качества"
            elif 'щебен' in category_name or 'щебн' in category_name:
                products_section_title = "Щебень различных фракций"
            elif 'песок' in category_name:
                products_section_title = "Песок для любых строительных работ"
            elif 'грунт' in category_name:
                products_section_title = "Плодородный грунт для вашего участка"
            elif 'асфальт' in category_name:
                products_section_title = "Качественный асфальт для дорожных работ"
            elif 'отсев' in category_name:
                products_section_title = "Отсев для устройства оснований"
            else:
                # Если категория не подходит под конкретную тему
                products_section_title = f"Строительные материалы для работы с {post.category.name}"

        # Если не удалось определить по категории, пробуем по заголовку статьи
        else:
            title_lower = post.title.lower()

            if 'бетон' in title_lower:
                products_section_title = "Бетонные смеси для вашего строительства"
            elif 'нерудн' in title_lower:
                products_section_title = "Нерудные материалы высокого качества"
            elif 'щебен' in title_lower or 'щебн' in title_lower:
                products_section_title = "Щебень различных фракций"
            elif 'песок' in title_lower:
                products_section_title = "Песок для любых строительных работ"
            elif 'грунт' in title_lower:
                products_section_title = "Плодородный грунт для вашего участка"
            elif 'асфальт' in title_lower:
                products_section_title = "Качественный асфальт для дорожных работ"
            elif 'отсев' in title_lower:
                products_section_title = "Отсев для устройства оснований"

        context['products_section_title'] = products_section_title

        # Настройка SEO
        context['title'] = post.title
        context['seo_title'] = post.meta_title or post.title
        context['seo_description'] = post.meta_description or post.excerpt
        context['seo_keywords'] = post.meta_keywords

        # Формируем хлебные крошки для статьи
        breadcrumbs = [
            {'title': 'Главная', 'url': reverse('home')},
            {'title': 'Блог', 'url': reverse('blog')},
        ]

        if post.category:
            breadcrumbs.append({
                'title': post.category.name,
                'url': reverse('blog_category', kwargs={'category_slug': post.category.slug}),
            })

        breadcrumbs.append({
            'title': post.title,
            'url': '',  # Текущая страница
        })

        context['breadcrumbs'] = breadcrumbs

        return context


# Функция для обычного представления блога
def blog(request):
    # Просто перенаправляем на класс-представление
    view = BlogListView.as_view()
    return view(request)


# Функция для отображения статей определенной категории
def blog_category(request, category_slug):
    view = BlogListView.as_view()
    return view(request, category_slug=category_slug)


# Функция для отображения статей с определенным тегом
def blog_tag(request, tag_slug):
    view = BlogListView.as_view()
    return view(request, tag_slug=tag_slug)


# Функция для отображения конкретной статьи
def blog_post(request, post_slug):
    view = PostDetailView.as_view()
    return view(request, post_slug=post_slug)