# Техническая документация проекта "ТД Ленинградский"

## 1. Архитектура проекта

### 1.1. Общий обзор архитектуры

Проект построен на основе фреймворка Django и следует паттерну MVT (Model-View-Template):
- **Model**: модели данных в Django ORM
- **View**: представления, обрабатывающие запросы
- **Template**: шаблоны для отображения данных

Архитектурно проект разделен на несколько приложений Django, каждое из которых отвечает за определенный функциональный блок:

```
new_tdl_site/               # Основной проект
├── blog/                   # Блог
├── cart/                   # Корзина и заказы
├── commonpages/            # Общие страницы сайта
├── good/                   # Товары и категории
├── leads/                  # Лиды и интеграция с Telegram
└── templates/              # Общие шаблоны
```

### 1.2. Схема базы данных

#### Приложение `good`
- **Product**: товары
- **Category**: категории товаров
- **City**: города для фильтрации товаров

#### Приложение `blog`
- **Post**: статьи блога
- **Category**: категории блога
- **Tag**: теги для статей

#### Приложение `cart`
- **Cart**: корзина покупок
- **CartItem**: товары в корзине
- **Order**: заказы
- **OrderItem**: товары в заказе

#### Приложение `leads`
- **Call**: заявки
- **Result**: результаты обработки заявок
- **Manager**: менеджеры
- **Good**: товары в заявках
- **CallItem**: товары в заявке

#### Приложение `commonpages`
- **CallbackRequest**: запросы на обратный звонок
- **FeedbackRequest**: запросы обратной связи
- **Redirect**: редиректы для SEO

### 1.3. Взаимодействие компонентов

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│    Клиент       │────▶│  Веб-сервер  │────▶│Django (WSGI)  │
│  (Браузер)      │◀────│   (Nginx)    │◀────│    Gunicorn   │
└─────────────────┘     └──────────────┘     └───────┬───────┘
                                                      │
                                                      ▼
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│   База данных   │◀────│   Модели     │◀────│Представления  │
│  (PostgreSQL)   │────▶│   Django     │────▶│    Views      │
└─────────────────┘     └──────────────┘     └───────┬───────┘
                                                      │
                                                      ▼
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│  Celery Worker  │◀────│ Celery Beat  │     │   Шаблоны     │
│  (Асинхронные   │────▶│ (Планировщик)│     │  Templates    │
│    задачи)      │     └──────────────┘     └───────────────┘
└─────────────────┘
```

## 2. Модели данных

### 2.1. Приложение `good`

#### Product
```python
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL", db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    product_card_description = models.TextField(blank=True, verbose_name="Описание в карточке")
    product_card_property = models.TextField(blank=True, verbose_name="Свойства в карточке")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    on_stock = models.BooleanField(default=True, verbose_name="В наличии")
    img = models.ImageField(upload_to="good/goods_images", blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория", related_name="products")
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="Город", related_name="products", blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
```

#### Category
```python
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategories", verbose_name="Родительская категория")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    small_text_for_catalog = models.TextField(blank=True, verbose_name="Короткое описание под title каталога")
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
```

#### City
```python
class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название города")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL")
    region = models.CharField(max_length=255, verbose_name="Регион", blank=True, null=True)
```

### 2.2. Приложение `blog`

#### Post
```python
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL статьи")
    content = HTMLField(verbose_name="Контент статьи")
    excerpt = models.TextField(blank=True, verbose_name="Краткое саммари в карточке")
    image = models.ImageField(upload_to='blog/images/%Y/%m/', blank=True, verbose_name="Изображение")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Теги")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name="Meta Keywords")
```

#### Category блога
```python
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
```

#### Tag
```python
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL тега")
```

### 2.3. Приложение `cart`

#### Cart
```python
class Cart(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### CartItem
```python
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
```

#### Order
```python
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipping', 'Доставляется'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    customer_name = models.CharField(max_length=255, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Email клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    shipping_address = models.TextField(verbose_name="Адрес доставки")
    city = models.CharField(max_length=100, verbose_name="Город")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
```

#### OrderItem
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
```

### 2.4. Приложение `leads`

#### Call
```python
class Call(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name='Дата звонка')
    resource = models.CharField(max_length=50, verbose_name='Источник', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    mail = models.EmailField(verbose_name='Электронная почта', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Организация/ЧЛ', null=True, blank=True)
    result = models.ForeignKey(to=Result, on_delete=models.CASCADE, verbose_name='Результат')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    manager = models.ForeignKey(to=Manager, on_delete=models.CASCADE, verbose_name='Менеджер')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    date_of_notification = models.DateField(null=True, blank=True, verbose_name='Дата уведомления')
```

#### Manager
```python
class Manager(models.Model):
    name = models.CharField(max_length=50, verbose_name='Менеджер', null=True, blank=True)
    mail = models.EmailField(verbose_name='Электронная почта менеджера', null=True, blank=True)
    tg_id = models.BigIntegerField(verbose_name='ID в Телеграм', null=True, blank=True)
```

#### Result
```python
class Result(models.Model):
    name = models.CharField(max_length=50, verbose_name='Результат')
```

### 2.5. Приложение `commonpages`

#### CallbackRequest
```python
class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### FeedbackRequest
```python
class FeedbackRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Товар")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
```

#### Redirect
```python
class Redirect(models.Model):
    old_path = models.CharField(_('Старый путь'), max_length=255, db_index=True)
    new_path = models.CharField(_('Новый путь'), max_length=255)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлен'), auto_now=True)
```

## 3. Представления (Views)

### 3.1. Приложение `good`

#### Каталог товаров
```python
def product(request, city_slug):
    # Получение города
    city = get_object_or_404(City, slug=city_slug)
    
    # Получение продуктов с оптимизацией
    products = Product.objects.select_related('category', 'city').filter(city=city)
    
    # Условное формирование заголовка
    if city.region:
        title = f"Товарный каталог продукции ТД Ленинградский в {city.region}: город {city.name}"
    else:
        title = f"Товарный каталог продукции ТД Ленинградский в городе {city.name}"
        
    # Формирование данных для контекста
    data = {
        "title": title,
        "products": products,
        # ...
    }
    
    # Рендеринг шаблона
    return render(request, "good/products.html", context=data)
```

#### Детальная страница товара
```python
def show_product(request, city_slug, category_slug, product_slug):
    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    try:
        good = Product.objects.select_related('category', 'city').get(
            slug=product_slug, 
            category=category, 
            city=city
        )
    except Product.DoesNotExist:
        good = None

    if good:
        related_goods = Product.objects.select_related('category', 'city').filter(
            category=category, 
            city=city
        ).exclude(id=good.id)[:3]
        # ...
```

### 3.2. Приложение `blog`

#### Список статей
```python
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
```

#### Детальная страница статьи
```python
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
```

### 3.3. Приложение `cart`

#### Корзина
```python
def cart_detail(request):
    """View for displaying the cart and its items"""
    session_cart = SessionCart(request)

    # Prepare the form to update quantities
    for item in session_cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'override': True})

    return render(request, 'cart/cart_detail.html', {
        'cart': session_cart,
        'title': 'Корзина - ТД Ленинградский',
        'seo_title': 'Корзина товаров - ТД Ленинградский',
        'seo_description': 'Просмотр и редактирование товаров в корзине перед оформлением заказа.',
    })
```

#### Оформление заказа
```python
def checkout(request):
    """Отображение формы оформления и обработка создания заказа"""
    session_cart = SessionCart(request)

    # Проверяем, пуста ли корзина
    if len(session_cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        # Получаем токен reCAPTCHA
        recaptcha_token = request.POST.get('g-recaptcha-response', '')

        # Проверяем токен reCAPTCHA только если форма прошла другие проверки
        if form.is_valid():
            # Проверка reCAPTCHA v3
            if not recaptcha_token:
                form.add_error(None, "Пожалуйста, перезагрузите страницу и попробуйте снова.")
                return render(request, 'cart/checkout.html', {
                    'cart': session_cart,
                    'form': form,
                    'title': 'Оформление заказа - ТД Ленинградский',
                    'seo_title': 'Оформление заказа - ТД Ленинградский',
                    'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                })

            recaptcha_valid, recaptcha_score = validate_recaptcha_v3(recaptcha_token)

            # Если проверка не пройдена или низкий балл (вероятно бот)
            if not recaptcha_valid or recaptcha_score < 0.5:
                form.add_error(None, "Проверка безопасности не пройдена. Пожалуйста, попробуйте еще раз.")
                return render(request, 'cart/checkout.html', {
                    # ...
                })

            # Все проверки пройдены, создаём заказ
            order = form.save(commit=False)
            # Устанавливаем общую стоимость
            order.total_cost = session_cart.get_total_price()
            # Отключаем автоматическую отправку уведомлений
            order.save(send_notification=False)

            # Добавляем товары заказа
            for item in session_cart:
                if 'product' in item:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

            # Отправляем уведомления после создания всех товаров
            from cart.signals import send_admin_notification, send_customer_confirmation
            send_admin_notification(order)
            send_customer_confirmation(order)

            # Очищаем корзину
            session_cart.clear()

            # Сохраняем ID заказа в сессии для страницы благодарности
            request.session['order_id'] = order.id

            # Перенаправляем на страницу успеха
            return redirect('cart:order_success')
```

### 3.4. API для интеграции с Telegram-ботом

```python
# Получает весь список заявок по GET запросу api/v1/callslist/ и может добавлять новую заявку по POST запросу
class CallsApiList(generics.ListCreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

# Получает одну заявку по id api/v1/callslist/call/<int:pk>/
class CallsDetailView(generics.RetrieveAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def get_object(self):
        object = super().get_object()
        if object is None:
            raise NotFound('Звонок не найден')
        return object

# Получает список заявок по id менеджера api/v1/callslist/manager-tg/<int:tg_id>/
class CallsByManagerTgIdApiList(generics.ListCreateAPIView):
    serializer_class = CallSerializer

    def get_queryset(self):
        tg_id = self.kwargs['tg_id']
        return Call.objects.filter(manager__tg_id=tg_id)
```

## 4. Асинхронные задачи (Celery)

### 4.1. Конфигурация Celery

```python
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_tdl_site.settings')
app = Celery('new_tdl_site')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-notifications-every-day': {
        'task': 'leads.tasks.check_notifications',
        'schedule': crontab(hour='12', minute='00'),
    },
}
```

### 4.2. Проверка уведомлений

```python
@shared_task
def check_notifications():
    today = date.today()
    calls = Call.objects.filter(date_of_notification=today)
    lost_calls = Call.objects.filter(date_of_notification__lt=today)

    # Группируем заявки по менеджеру
    calls_by_manager = {}
    for call in calls:
        manager = call.manager
        if manager not in calls_by_manager:
            calls_by_manager[manager] = []
        calls_by_manager[manager].append(call)

    # Отправляем уведомления для сегодняшних заявок
    for manager, manager_calls in calls_by_manager.items():
        user_id = manager.tg_id
        message = (
            f"Уважаемый(ая), {manager.name}\n\n"
            f"Сегодня {today} подходит срок исполнения заявок:\n"
        )
        for call in manager_calls:
            message += (
                f'Заявка № {call.id} от {call.created}\n'
                f'Клиент: {call.name}\n'
                f'Телефон: {call.phone}\n'
                f'Комментарий: {call.comment}\n\n'
            )
        if user_id and message:
            send_telegram_message(user_id, message)
```

## 5. Middleware

### 5.1. CityMiddleware

```python
class CityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        city_slug = request.session.get('city_slug')
        if not city_slug:
            request.cities = City.objects.all()
        else:
            request.city_slug = city_slug
        response = self.get_response(request)
        return response
```

### 5.2. RedirectMiddleware

```python
class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем редиректы для админки
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Получаем редиректы из кэша
        redirects = cache.get('redirects')
        if redirects is None:
            redirects = {
                r.old_path: r.new_path
                for r in Redirect.objects.filter(is_active=True)
            }
            cache.set('redirects', redirects, 60 * 60)  # Кэшируем на 1 час

        # Нормализуем текущий путь
        path = request.path
        if not path.startswith('/'):
            path = '/' + path

        # Проверяем пути с разными вариантами окончания
        path_variants = [path]
        if path.endswith('/'):
            path_variants.append(path[:-1])
        else:
            path_variants.append(path + '/')

        # Проверяем все варианты пути
        for path_variant in path_variants:
            if path_variant in redirects:
                new_path = redirects[path_variant]
                # Если новый путь относительный, добавляем ведущий слеш
                if not new_path.startswith(('http://', 'https://', '/')):
                    new_path = '/' + new_path
                return redirect(new_path, permanent=True)

        return self.get_response(request)
```

### 5.3. ApiTokenMiddleware

```python
class ApiTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_token = request.headers.get('Authorization')
        # Проверяем наличие заголовка Authorization
            if api_token is None or api_token != f'{settings.API_TOKEN}':
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        return self.get_response(request)
```

## 6. Контекстные процессоры

### 6.1. Menu Context Processor

```python
def default_context(request):
    return {
        'menu': [
            {'title': 'О компании', 'url_name': 'about'},
            {'title': 'Контакты', 'url_name': 'contacts'},
            {'title': 'Продукция', 'url_name': 'catalog'},
            {
                'title': 'Услуги',
                'url_name': 'services',
                'children': [
                    {'title': 'Калькулятор доставки', 'url_name': 'delivery'},
                    {'title': 'Калькулятор бетона',
                     'url_name': 'concrete_calculator'},
                ]
            },
            {'title': 'Блог', 'url_name': 'blog'},
        ],
    }
```

### 6.2. City Context Processor

```python
def city_context(request):
    DEFAULT_CITY_SLUG = 'mariupol'
    city_slug = request.session.get('city_slug', DEFAULT_CITY_SLUG)
    city = City.objects.filter(slug=city_slug).first()
    if not city:
        city = City.objects.filter(slug=DEFAULT_CITY_SLUG).first()
    return {
        'city_slug': city.slug,
        'city_name': city.name,
        'cities': City.objects.all(),
        'city_slugs': list(City.objects.values_list('slug', flat=True)),
    }
```
## 7. Шаблоны и статические файлы

### 7.1. Структура шаблонов

```
templates/
├── 404.html                  # Страница 404 ошибки
├── base.html                 # Базовый шаблон
├── includes/                 # Подключаемые части шаблонов
│   ├── city_modal.html       # Модальное окно выбора города
│   ├── footer.html           # Футер сайта
│   ├── header.html           # Хедер сайта
│   ├── popup_cart.html       # Всплывающая корзина
│   └── telegram-popup.html   # Всплывающее окно Telegram
├── robots.txt                # Файл robots.txt
└── sitemap_with_images.xml   # Шаблон для Sitemap с изображениями
```

### 7.2. Базовый шаблон

Базовый шаблон `base.html` содержит основную структуру страницы:
- DOCTYPE, мета-теги, OG-теги
- Подключение CSS и JavaScript
- Включение блоков хедера и футера
- Блок контента, который переопределяется в дочерних шаблонах
- Подключение модальных окон

### 7.3. Статические файлы

```
static/
├── css/                     # CSS стили
│   ├── animations.css       # Анимации
│   ├── blog.css             # Стили для блога
│   ├── cart.css             # Стили для корзины
│   ├── dividers.css         # Стили для разделителей
│   ├── modal.css            # Стили для модальных окон
│   ├── popup_cart.css       # Стили для всплывающей корзины
│   ├── styles.css           # Основные стили
│   └── telegram-popup.css   # Стили для Telegram попапа
├── images/                  # Изображения
└── js/                      # JavaScript файлы
    ├── animations.js        # Анимации
    ├── cart.js              # Корзина и заказы
    ├── cityModal.js         # Модальное окно выбора города
    ├── concreteCalculator.js # Калькулятор бетона
    ├── contactsMapChanger.js # Смена карт на странице контактов
    ├── deliveryCalculator.js # Калькулятор доставки
    ├── dividers.js          # Разделители
    ├── feedbackForm.js      # Обработка формы обратной связи
    ├── header/              # Скрипты для хедера
    │   ├── cityDropdown.js  # Выпадающее меню городов
    │   ├── headerCallbackPopup.js # Попап обратного звонка
    │   └── headerNavDisplay.js # Отображение навигации
    └── telegram-popup.js    # Всплывающее окно Telegram
```

## 8. URL-маршрутизация

### 8.1. Основные URL-маршруты

```python
# new_tdl_site/urls.py
urlpatterns = [
    path('tdladmin/', admin.site.urls),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('catalog/', include('good.urls')),
    path('', include('commonpages.urls')),
    path('', include('blog.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemap_with_images.xml'}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]
```

### 8.2. Маршруты приложения good

```python
# good/urls.py
urlpatterns = [
    path('<slug:city_slug>/', views.product, name='catalog'),
    path('<slug:city_slug>/<slug:category_slug>/', views.show_category, name='category'),
    path('<slug:city_slug>/<slug:category_slug>/<slug:product_slug>/', views.show_product, name='product'),
]
```

### 8.3. Маршруты приложения blog

```python
# blog/urls.py
urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('blog/tag/<slug:tag_slug>/', views.blog_tag, name='blog_tag'),
    path('blog/<slug:post_slug>/', views.blog_post, name='blog_post'),
]
```

### 8.4. Маршруты приложения cart

```python
# cart/urls.py
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('summary/', views.cart_summary, name='cart_summary'),
]
```

### 8.5. API-маршруты для Telegram-бота

```python
urlpatterns = [
    path('api/v1/callslist/', CallsApiList.as_view()), # список заявок и добавление заявок
    path('api/v1/managers/', ManagersApiList.as_view()), # список менеджеров
    path('api/v1/results/', ResultsApiList.as_view()), # список результатов
    path('api/v1/callslist/<int:pk>/', CallsApiUpdate.as_view()), # обновление заявки
    path('api/v1/callslist/call/<int:pk>/', CallsDetailView.as_view()), # получение данных заявки
    path('api/v1/callslist/manager-tg/<int:tg_id>/', CallsByManagerTgIdApiList.as_view()), # заявки менеджера
    path('api/v1/callslist/manager-tg/<int:tg_id>/<int:pk>/', CallsByManagerTgIdApiUpdate.as_view()), # обновление заявки менеджера
    path('api/v1/callslist/filter/', CallByManagerTgIdAndDateRangeApiList.as_view()), # фильтрация заявок
    path('api/v1/callslist/comment_update/<int:pk>/', CallCommentUpdateView.as_view()), # обновление комментария
    path('api/v1/callslist/result_update/<int:pk>/', CallResultUpdateView.as_view()), # обновление статуса
    path('api/v1/callslist/manager_update/<int:pk>/', CallManagerUpdateView.as_view()), # обновление менеджера
]
```

## 9. Интеграция с внешними сервисами

### 9.1. Интеграция с Telegram

#### 9.1.1. Отправка сообщений в Telegram

```python
def send_telegram_message(user_id, message, reply_markup=None):
    bot_token = BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'HTML'  # Опционально, если использовать HTML в сообщении
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)

    response = requests.post(url, data=data)
    return response.json()
```

#### 9.1.2. Клавиатура для действий в Telegram

```python
def action_choice_keyboard(task_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Добавить комментарий",
                 "callback_data": f"edit_comment:{task_id}"}
            ],
            [
                {"text": "Изменить статус",
                 "callback_data": f"edit_status:{task_id}"}
            ],
            [
                {"text": "Передать другому менеджеру",
                 "callback_data": f"edit_manager:{task_id}"}
            ],
        ]
    }
    return keyboard
```

### 9.2. Интеграция с reCAPTCHA

```python
def validate_recaptcha_v3(token):
    """Проверка токена reCAPTCHA v3 с Google"""
    if not token:
        return False, 0.0

    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        success = result.get('success', False)
        score = result.get('score', 0.0)  # reCAPTCHA v3 возвращает оценку от 0.0 до 1.0

        return success, score
    except Exception as e:
        print(f"Ошибка при проверке reCAPTCHA: {e}")
        return False, 0.0
```

### 9.3. Интеграция с Яндекс.Картами

```javascript
ymaps.ready(init);

function init() {
    // Стоимость за км за м³ бетона (руб)
    const RATE_PER_KM_PER_M3 = 600;

    // Базовая точка доставки
    const BASE_POINT = [60.906882, 30.067233];

    // Инициализация карты
    const myMap = new ymaps.Map('map', {
        center: BASE_POINT,
        zoom: 9,
        controls: []
    });

    // Создаем панель маршрутизации
    const routePanelControl = new ymaps.control.RoutePanel({
        options: {
            showHeader: true,
            title: 'Расчёт доставки'
        }
    });

    // Добавляем элементы управления на карту
    myMap.controls.add(routePanelControl).add(new ymaps.control.ZoomControl({
        options: {
            size: 'small',
            float: 'none',
            position: {
                bottom: 145,
                right: 10
            }
        }
    }));

    // Задаем неизменяемую точку "откуда"
    routePanelControl.routePanel.state.set({
        fromEnabled: false,
        from: 'Мариуполь, улица Сортировочная 1'
    });
    
    // ...
}
```

### 9.4. Интеграция с электронной почтой

```python
@receiver(post_save, sender=Order)
def notify_on_order_creation(sender, instance, created, **kwargs):
    """Send email notifications when an order is created"""
    send_notification = instance.__dict__.get('_send_notification', True)

    if created and send_notification:
        # Send email to admin
        send_admin_notification(instance)

        # Send confirmation to customer
        send_customer_confirmation(instance)


def send_admin_notification(order):
    """Send notification email to administrators"""
    subject = f'Новый заказ №{order.id} на сайте ТД Ленинградский'

    # Принудительно загружаем товары заказа заранее
    order_items = list(order.items.select_related('product').all())

    # Create HTML message with context
    context = {
        'order': order,
        'order_items': order_items,
        'site_url': settings.SITE_URL,
    }

    html_message = render_to_string('cart/email/admin_notification.html', context)
    plain_message = strip_tags(html_message)

    # Send email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления администратору о заказе #{order.id}: {str(e)}")
```

## 10. SEO-оптимизация

### 10.1. Sitemap

```python
# Sitemap для статических страниц
class StaticViewSitemap(Sitemap):
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
        return datetime.datetime.now()

    def image(self, item):
        images = {
            'home': 'static/images/logo/logo.svg',
        }
        return [images[item]] if item in images else []


# Sitemap для товаров
class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.time_update

    def location(self, obj):
        return obj.get_absolute_url()

    def image(self, obj):
        if obj.img:
            return [obj.img.url]
        return []


# Sitemap для категорий товаров
class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        # Генерируем комбинации городов и категорий, где есть товары
        items = []
        cities = City.objects.all()
        categories = Category.objects.all()
        for city in cities:
            for category in categories:
                # Проверяем, есть ли продукты в данной категории и городе
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


# Sitemap для блога
class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return obj.get_absolute_url()
    
    def image(self, obj):
        if obj.image:
            return [obj.image.url]
        return []


# Sitemap для категорий блога
class BlogCategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return BlogCategory.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


# Sitemap для тегов блога
class BlogTagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
```

### 10.2. Микроразметка Schema.org

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{{ good.name|escapejs }}",
"description": "{{ good.description|striptags|escapejs }}",
{% if good.img %}
    "image": "{{ request.scheme }}://{{ request.get_host }}{{ good.img.url }}",
{% else %}
    "image": "{{ request.scheme }}://{{ request.get_host }}{% static 'images/mainpage/zavod.webp' %}",
{% endif %}
"brand": {
    "@type": "Brand",
    "name": "ТД Ленинградский"
},
"offers": {
    "@type": "Offer",
    "url": "{{ request.build_absolute_uri }}",
    "priceCurrency": "RUB",
    "price": {{ good.price|unlocalize }},
    "availability": "{% if good.on_stock %}InStock{% else %}OutOfStock{% endif %}",
    "itemCondition": "NewCondition",
    "availableDeliveryMethod": "http://purl.org/goodrelations/v1#DeliveryModeOwnFleet",
    "areaServed": {
        "@type": "City",
        "name": "{{ city.name|escapejs }}"
    }
},
"category": "{{ good.category.name|escapejs }}",
"sku": "{{ good.id }}",
"additionalProperty": {
    "@type": "PropertyValue",
    "name": "Характеристики",
    "value": "{{ good.product_card_property|striptags|escapejs }}"
}
}
</script>
```

### 10.3. Метатеги

```html
<title>
    {% block title %}
        {% if seo_title %}
            {{ seo_title }}
        {% else %}
            {{ title }}
        {% endif %}
    {% endblock %}
</title>
<meta name="description" content="{% if seo_description %}{{ seo_description }}{% else %}{{ seo_description }}{% endif %}">
<meta name="keywords" content="{% if seo_keywords %}{{ seo_keywords }}{% else %}{{ seo_keywords }}{% endif %}">
{% block og_meta %}
    <!-- Базовые OpenGraph метатеги, могут быть переопределены в дочерних шаблонах -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{% if seo_title %}{{ seo_title }}{% else %}{{ title }}{% endif %}">
    <meta property="og:description" content="{% if seo_description %}{{ seo_description }}{% else %}{{ seo_description }}{% endif %}">
    <meta property="og:url" content="{{ request.build_absolute_uri }}">
    <meta property="og:site_name" content="ТД Ленинградский">
{% endblock %}
```

### 10.4. robots.txt

```
User-Agent: *
Disallow: /tdladmin/
Disallow: /privacy/
Disallow: /static/
Disallow: /cart/
Allow: /static/images/

Clean-param: etext&yadiscount

Sitemap: https://tdleningrad.ru/sitemap.xml
```

## 11. Безопасность

### 11.1. Защита API с помощью токенов

```python
class ApiTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_token = request.headers.get('Authorization')
            if api_token is None or api_token != f'{settings.API_TOKEN}':
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        return self.get_response(request)
```

### 11.2. reCAPTCHA для форм

```javascript
document.getElementById('callback-form').addEventListener('submit', function(e) {
    e.preventDefault();

    let form = this;
    let url = this.getAttribute('data-url');

    let submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    grecaptcha.ready(function() {
        grecaptcha.execute('RECAPTCHA_SITE_KEY', {action: 'submit'}).then(function(token) {
            let formData = new FormData(form);
            formData.append('g-recaptcha-response', token);

            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => response.json())
            .then(data => {
                // Обработка ответа
            })
            .catch(error => {
                console.error('Ошибка:', error);
                submitButton.disabled = false;
            });
        });
    });
});
```

### 11.3. Honeypot-поля

```html
<div class="honeypot-field">
    {{ form.website }}
</div>
```

```python
class OrderCreateForm(forms.ModelForm):
    """Form for creating an order"""
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Я согласен с условиями обработки персональных данных"
    )

    # honeypot
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="Ловушка"
    )

    def clean_website(self):
        """Проверка поля-ловушки"""
        website = self.cleaned_data.get('website')
        if website:
            # Если поле-ловушка заполнено, это, вероятно, бот
            raise forms.ValidationError("Обнаружен бот.")
        return website
```

### 11.4. CSRF-защита

```html
<form id="city-form" method="post" action="{% url 'set_city' %}">
    {% csrf_token %}
    <select name="city_slug" required>
        {% for city in cities %}
            <option value="{{ city.slug }}"
                    {% if city.slug == city_slug %}
                    selected
                    {% endif %}>
                {{ city.name }}
            </option>
        {% endfor %}
    </select>
    <button type="submit">Выбрать</button>
</form>
```

## 12. Развертывание проекта

### 12.1. Настройка Gunicorn

```python
# Файл: config/gunicorn.conf.py
bind = '127.0.0.1:8000'
workers = 2
user = 'igor'
timeout = 120
```

### 12.2. Настройка Nginx

```nginx
# Конфигурация для HTTPS
server {
    listen 443 ssl http2;
    server_name tdleningrad.ru www.tdleningrad.ru;

    ssl_certificate /etc/letsencrypt/live/tdleningrad.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tdleningrad.ru/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Кеширование OCSP
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # Дополнительные заголовки безопасности
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";
    
    # Статические файлы
    location /static/ {
        alias /home/igor/new_tdl_site/static/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Медиа-файлы
    location /media/ {
        alias /home/igor/new_tdl_site/media/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Проксирование запросов к Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 8 8k;
        
        proxy_read_timeout 120s;
        proxy_connect_timeout 75s;
    }
    
    # Логи
    access_log /var/log/nginx/tdleningrad.access.log;
    error_log /var/log/nginx/tdleningrad.error.log error;
}

# Редирект с HTTP на HTTPS
server {
    listen 80;
    server_name tdleningrad.ru www.tdleningrad.ru;
    
    location / {
        return 301 https://$host$request_uri;
    }
}
```

### 12.3. Настройка Supervisor

```ini
[program:tdleningrad]
command=/home/igor/venv/bin/gunicorn -c /home/igor/new_tdl_site/config/gunicorn.conf.py new_tdl_site.wsgi:application
directory=/home/igor/new_tdl_site
user=igor
autostart=true
autorestart=true
startretries=5
stdout_logfile=/home/igor/logs/gunicorn_stdout.log
stderr_logfile=/home/igor/logs/gunicorn_stderr.log
environment=PATH="/home/igor/venv/bin"

[program:tdleningrad_celery]
command=/home/igor/venv/bin/celery -A new_tdl_site worker --loglevel=info
directory=/home/igor/new_tdl_site
user=igor
numprocs=1
autostart=true
autorestart=true
startsecs=10
startretries=5
stdout_logfile=/home/igor/logs/celery_worker.log
stderr_logfile=/home/igor/logs/celery_worker.log
environment=PATH="/home/igor/venv/bin"

[program:tdleningrad_celery_beat]
command=/home/igor/venv/bin/celery -A new_tdl_site beat --loglevel=info
directory=/home/igor/new_tdl_site
user=igor
numprocs=1
autostart=true
autorestart=true
startsecs=10
startretries=5
stdout_logfile=/home/igor/logs/celery_beat.log
stderr_logfile=/home/igor/logs/celery_beat.log
environment=PATH="/home/igor/venv/bin"
```

### 12.4. Настройки для Production

```python
# Настройки для Production
DEBUG = False

ALLOWED_HOSTS = ['tdleningrad.ru', 'www.tdleningrad.ru']

STATIC_ROOT = os.path.join(BASE_DIR, "static")

CSRF_TRUSTED_ORIGINS = ['https://tdleningrad.ru']

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 13. Тесты

Хотя в проекте есть файлы для тестов в каждом приложении, они не реализованы в полной мере. Ниже представлены примеры тестов, которые можно реализовать:

### 13.1. Тесты моделей

```python
from django.test import TestCase
from good.models import Product, Category, City

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        city = City.objects.create(name='Test City', slug='test-city')
        category = Category.objects.create(name='Test Category', slug='test-category')
        Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=100.00,
            category=category,
            city=city
        )

    def test_product_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_product_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEqual(
            product.get_absolute_url(),
            '/test-city/test-category/test-product/'
        )
```

### 13.2. Тесты представлений

```python
from django.test import TestCase, Client
from django.urls import reverse
from good.models import Product, Category, City

class ProductViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        city = City.objects.create(name='Test City', slug='test-city')
        category = Category.objects.create(name='Test Category', slug='test-category')
        Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=100.00,
            category=category,
            city=city
        )

    def setUp(self):
        self.client = Client()

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog', args=['test-city']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'good/products.html')
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 1)

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product', args=['test-city', 'test-category', 'test-product'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'good/good.html')
        self.assertTrue('good' in response.context)
        self.assertEqual(response.context['good'].name, 'Test Product')
```

### 13.3. Тесты форм

```python
from django.test import TestCase
from cart.forms import CartAddProductForm, OrderCreateForm

class CartAddProductFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'quantity': 5,
            'override': True
        }
        form = CartAddProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'quantity': 'not_a_number',
            'override': True
        }
        form = CartAddProductForm(data=data)
        self.assertFalse(form.is_valid())

class OrderCreateFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'customer_name': 'Test Customer',
            'customer_email': 'test@example.com',
            'customer_phone': '+79001234567',
            'city': 'Test City',
            'shipping_address': 'Test Address',
            'agree_to_terms': True
        }
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        data = {
            'customer_name': '',
            'customer_email': '',
            'customer_phone': '',
            'city': '',
            'shipping_address': '',
            'agree_to_terms': False
        }
        form = OrderCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('customer_name' in form.errors)
        self.assertTrue('customer_email' in form.errors)
        self.assertTrue('customer_phone' in form.errors)
        self.assertTrue('city' in form.errors)
        self.assertTrue('shipping_address' in form.errors)
        self.assertTrue('agree_to_terms' in form.errors)
```

### 13.4. Тесты API

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from leads.models import Call, Result, Manager
import json

class CallAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        result = Result.objects.create(name='Новый')
        manager = Manager.objects.create(name='Test Manager', tg_id=123456789)
        Call.objects.create(
            phone='+79001234567',
            name='Test Client',
            result=result,
            manager=manager
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='test-token')

    def test_get_calls_list(self):
        response = self.client.get(reverse('calls-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_call(self):
        result = Result.objects.get(pk=1)
        manager = Manager.objects.get(pk=1)
        data = {
            'phone': '+79009876543',
            'name': 'New Test Client',
            'result': result.id,
            'manager': manager.id
        }
        response = self.client.post(
            reverse('calls-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Call.objects.count(), 2)
```

## 14. Обслуживание и поддержка

### 14.1. Резервное копирование

#### 14.1.1. Резервное копирование базы данных

```bash
#!/bin/bash

# Настройки
DB_NAME="tdleningrad_db"
DB_USER="tdleningrad_user"
BACKUP_DIR="/home/igor/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

# Создаем директорию для резервных копий, если она не существует
mkdir -p $BACKUP_DIR

# Создаем резервную копию и сжимаем ее
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_FILE

# Проверяем успешность выполнения
if [ $? -eq 0 ]; then
    echo "Резервное копирование успешно создано: $BACKUP_FILE"
else
    echo "Ошибка при создании резервной копии!"
    exit 1
fi

# Удаляем старые резервные копии (оставляем последние 10)
ls -t $BACKUP_DIR/db_backup_*.sql.gz | tail -n +11 | xargs -r rm

echo "Очистка старых резервных копий завершена."
```

#### 14.1.2. Резервное копирование файлов

```bash
#!/bin/bash

# Настройки
PROJECT_DIR="/home/igor/new_tdl_site"
BACKUP_DIR="/home/igor/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz"

# Создаем директорию для резервных копий, если она не существует
mkdir -p $BACKUP_DIR

# Создаем резервную копию статических и медиа-файлов
tar -czf $BACKUP_FILE -C $PROJECT_DIR static media

# Проверяем успешность выполнения
if [ $? -eq 0 ]; then
    echo "Резервное копирование файлов успешно создано: $BACKUP_FILE"
else
    echo "Ошибка при создании резервной копии файлов!"
    exit 1
fi

# Удаляем старые резервные копии (оставляем последние 5)
ls -t $BACKUP_DIR/files_backup_*.tar.gz | tail -n +6 | xargs -r rm

echo "Очистка старых резервных копий файлов завершена."
```

### 14.2. Мониторинг

#### 14.2.1. Мониторинг Django-приложения

```python
INSTALLED_APPS = [
    # ...
    'django_prometheus',
    # ...
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ...
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]
```

#### 14.2.2. Мониторинг сервера

```bash
#!/bin/bash

# Проверка загрузки CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
CPU_THRESHOLD=80

# Проверка использования памяти
MEM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
MEM_THRESHOLD=90

# Проверка использования диска
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_THRESHOLD=85

# Проверка количества процессов
PROCESS_COUNT=$(ps aux | wc -l)
PROCESS_THRESHOLD=500

# Проверка активности веб-сервера
WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://tdleningrad.ru)

# Отправка уведомления
send_notification() {
    local message="$1"
    # Отправка сообщения в Telegram
    curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
        -d chat_id=$ADMIN_CHAT_ID \
        -d text="$message" > /dev/null
}

# Проверка и отправка уведомлений
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    send_notification "ВНИМАНИЕ: Высокая загрузка CPU на сервере: ${CPU_USAGE}%"
fi

if (( $(echo "$MEM_USAGE > $MEM_THRESHOLD" | bc -l) )); then
    send_notification "ВНИМАНИЕ: Высокое использование памяти: ${MEM_USAGE}%"
fi

if (( DISK_USAGE > DISK_THRESHOLD )); then
    send_notification "ВНИМАНИЕ: Высокое использование диска: ${DISK_USAGE}%"
fi

if (( PROCESS_COUNT > PROCESS_THRESHOLD )); then
    send_notification "ВНИМАНИЕ: Большое количество процессов: ${PROCESS_COUNT}"
fi

if [[ "$WEB_STATUS" != "200" ]]; then
    send_notification "КРИТИЧЕСКАЯ ОШИБКА: Веб-сервер недоступен! Код ответа: ${WEB_STATUS}"
fi

# Логирование
echo "$(date) - CPU: ${CPU_USAGE}%, MEM: ${MEM_USAGE}%, DISK: ${DISK_USAGE}%, PROCESSES: ${PROCESS_COUNT}, WEB: ${WEB_STATUS}" >> /var/log/server_monitor.log
```

### 14.3. Обновление системы

```bash
#!/bin/bash

# Логирование
LOG_FILE="/var/log/tdleningrad_update.log"
echo "===== Обновление системы $(date) =====" >> $LOG_FILE

# Перейти в директорию проекта
cd /home/igor/new_tdl_site

# Активировать виртуальное окружение
source /home/igor/venv/bin/activate

# Остановить сервисы
echo "Останавливаем сервисы..." >> $LOG_FILE
sudo supervisorctl stop tdleningrad tdleningrad_celery tdleningrad_celery_beat

# Создать резервную копию базы данных
echo "Создание резервной копии базы данных..." >> $LOG_FILE
pg_dump -U tdleningrad_user tdleningrad_db > /home/igor/backups/pre_update_backup_$(date +%Y%m%d_%H%M%S).sql

# Получить последние изменения с репозитория
echo "Получение обновлений..." >> $LOG_FILE
git pull origin main >> $LOG_FILE 2>&1

# Обновить зависимости
echo "Обновление зависимостей..." >> $LOG_FILE
pip install -r requirements.txt >> $LOG_FILE 2>&1

# Применить миграции
echo "Применение миграций..." >> $LOG_FILE
python manage.py migrate >> $LOG_FILE 2>&1

# Собрать статические файлы
echo "Сборка статических файлов..." >> $LOG_FILE
python manage.py collectstatic --noinput >> $LOG_FILE 2>&1

# Очистить кэш
echo "Очистка кэша..." >> $LOG_FILE
python manage.py clear_cache >> $LOG_FILE 2>&1

# Запустить сервисы
echo "Запуск сервисов..." >> $LOG_FILE
sudo supervisorctl start tdleningrad tdleningrad_celery tdleningrad_celery_beat

# Проверка работоспособности
echo "Проверка работоспособности..." >> $LOG_FILE
sleep 5
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://tdleningrad.ru)
if [[ "$STATUS_CODE" == "200" ]]; then
    echo "Сайт доступен, обновление завершено успешно!" >> $LOG_FILE
else
    echo "ОШИБКА: Сайт недоступен после обновления! Код статуса: $STATUS_CODE" >> $LOG_FILE
    # Отправка уведомления об ошибке
    curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
        -d chat_id=$ADMIN_CHAT_ID \
        -d text="ОШИБКА: Сайт недоступен после обновления! Код статуса: $STATUS_CODE" > /dev/null
fi

echo "===== Завершение обновления $(date) =====" >> $LOG_FILE
```

## 15. Инструкции для разработчиков

### 15.1. Рабочий процесс разработки

1. **Создание ветки для новой функциональности**:
   ```bash
   git checkout -b feature/название-функции
   ```

2. **Внесение изменений и коммит**:
   ```bash
   git add .
   git commit -m "Добавлена новая функция: краткое описание"
   ```

3. **Отправка изменений в репозиторий**:
   ```bash
   git push origin feature/название-функции
   ```

4. **Создание Pull Request** для слияния ветки с основной веткой

5. **Код-ревью** от другого разработчика

6. **Слияние с основной веткой** после утверждения

### 15.2. Стандарты кода

#### 15.2.1. PEP 8

Проект следует стандарту PEP 8 для Python-кода. Используйте инструменты форматирования кода, такие как `black` и `flake8`:

```bash
# Форматирование кода с помощью black
black .

# Проверка стиля кода
flake8 .
```

#### 15.2.2. Документирование кода

Для документирования функций и классов используется docstring в формате Google:

```python
def function_name(param1, param2):
    """Краткое описание функции.

    Подробное описание функции, которое может занимать несколько строк.

    Args:
        param1 (тип): Описание первого параметра.
        param2 (тип): Описание второго параметра.

    Returns:
        тип: Описание возвращаемого значения.

    Raises:
        ИсключениеТипа: Описание исключения.
    """
    # Код функции
```

#### 15.2.3. Именование

- **Переменные и функции**: `snake_case` (все буквы строчные, слова разделены подчеркиваниями)
- **Классы**: `PascalCase` (каждое слово начинается с заглавной буквы, без разделителей)
- **Константы**: `UPPER_SNAKE_CASE` (все буквы заглавные, слова разделены подчеркиваниями)
- **Приватные методы/атрибуты**: начинаются с подчеркивания `_private_method`

### 15.3. Доступные команды для управления проектом

```bash
# Запуск сервера разработки
python manage.py runserver

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic

# Запуск тестов
python manage.py test

# Запуск shell
python manage.py shell

# Запуск Celery-воркера
celery -A new_tdl_site worker --loglevel=info

# Запуск Celery-планировщика
celery -A new_tdl_site beat --loglevel=info
```

## 16. Заключение

### 16.1. Контакты для поддержки

- **Администратор проекта**: admin@tdleningrad.ru
- **Технический директор**: tech@tdleningrad.ru
- **Служба поддержки**: support@tdleningrad.ru
- **Телефон поддержки**: +7 (949) 624-2644

### 16.2. Ссылки на дополнительные ресурсы

- [Документация Django](https://docs.djangoproject.com/)
- [Документация Django REST framework](https://www.django-rest-framework.org/)
- [Документация Celery](https://docs.celeryproject.org/)
- [Документация Nginx](https://nginx.org/en/docs/)
- [Документация Gunicorn](https://docs.gunicorn.org/)
- [Документация Supervisor](http://supervisord.org/)