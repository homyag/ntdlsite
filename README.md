# ТД Ленинградский - Корпоративный веб-сайт

[![Django](https://img.shields.io/badge/Django-5.1.9-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.4.0-37B24D?style=flat&logo=celery&logoColor=white)](https://celeryproject.org/)

> Корпоративный веб-сайт компании "ТД Ленинградский" - ведущего поставщика бетона и нерудных материалов в ДНР, ЛНР и Мариуполе.

## 🏗️ О проекте

Полнофункциональный веб-сайт с интернет-магазином, системой управления заказами, интеграцией с Telegram-ботом и аналитикой. Проект включает каталог продукции, блог, систему заявок и CRM-интеграцию.

### ✨ Основные возможности

- 🛒 **E-commerce платформа** с корзиной и системой заказов
- 📱 **Адаптивный дизайн** для всех устройств
- 📧 **Email-уведомления** клиентам и администраторам
- 🤖 **Telegram-бот интеграция** для управления заявками
- 📊 **Аналитика** с Яндекс.Метрикой
- 🔐 **reCAPTCHA защита** от спама
- 📝 **Блог-система** с категориями и тегами
- 🗺️ **Калькуляторы** доставки и объема бетона
- 🏙️ **Мультигородность** с геотаргетингом
- 🔍 **SEO-оптимизация** с sitemap и микроразметкой

## 🛠️ Технологический стек

### Backend
- **Django 5.1.9** - основной фреймворк
- **Django REST Framework** - API для Telegram-бота
- **PostgreSQL** - основная база данных
- **Redis** - кеширование и очереди
- **Celery** - асинхронные задачи

### Frontend
- **Vanilla JavaScript** - интерактивность
- **CSS3** с адаптивным дизайном
- **Яндекс.Карты API** - калькулятор доставки
- **reCAPTCHA v3** - защита форм

### Интеграции
- **Telegram Bot API** - уведомления и управление
- **Яндекс.Метрика** - веб-аналитика
- **SMTP Email** - уведомления
- **WhatsApp/Telegram** мессенджеры

## 📁 Структура проекта

```
new_tdl_site/
├── 📁 blog/                    # Блог-приложение
├── 📁 cart/                    # Корзина и заказы
├── 📁 commonpages/             # Основные страницы
├── 📁 good/                    # Каталог товаров
├── 📁 leads/                   # CRM и заявки
├── 📁 new_tdl_site/           # Настройки проекта
│   ├── 📄 settings.py         # Конфигурация Django
│   ├── 📄 urls.py            # URL-маршрутизация
│   ├── 📄 celery.py          # Настройки Celery
│   └── 📄 sitemap.py         # SEO Sitemap
├── 📁 static/                 # Статические файлы
│   ├── 📁 css/               # Стили
│   ├── 📁 js/                # JavaScript
│   └── 📁 images/            # Изображения
├── 📁 templates/              # HTML шаблоны
├── 📁 media/                  # Загруженные файлы
├── 📁 config/                 # Конфигурация сервера
├── 📄 requirements.txt        # Python зависимости
└── 📄 manage.py              # Django CLI
```

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8+
- PostgreSQL 13+
- Redis 6+
- Node.js (опционально, для минификации)

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-repo/new_tdl_site.git
cd new_tdl_site
```

### 2. Настройка виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` на основе `.env_example`:

```bash
cp .env_example .env
```

Заполните необходимые переменные:

```env
# Django
DJANGO_SECRET=your-secret-key-here
DEBUG=True

# База данных
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tdleningrad_db
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=5432

# API токены
BOT_TOKEN=your_telegram_bot_token
API_TOKEN=your_api_token
RECAPTCHA_SECRET_KEY=your_recaptcha_secret
RECAPTCHA_SITE_KEY=your_recaptcha_site_key

# Telegram
OPERATOR_TG_ID=your_operator_id
ADMIN_TG_ID=your_admin_id

# Email
EMAIL_HOST_PASSWORD=your_email_password
```

### 5. Настройка базы данных

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

### 6. Загрузка тестовых данных (опционально)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000

### 8. Запуск Celery (в отдельном терминале)

```bash
# Celery Worker
celery -A new_tdl_site worker --loglevel=info

# Celery Beat (планировщик)
celery -A new_tdl_site beat --loglevel=info
```

## 🔧 Конфигурация для продакшена

### Gunicorn + Nginx

1. **Настройка Gunicorn:**

```bash
# Создание конфигурации
cp config/gunicorn.conf.py.example config/gunicorn.conf.py

# Запуск
gunicorn -c config/gunicorn.conf.py new_tdl_site.wsgi:application
```

2. **Конфигурация Nginx:**

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/certificate.pem;
    ssl_certificate_key /path/to/private.key;
    
    location /static/ {
        alias /path/to/new_tdl_site/static/;
        expires 30d;
    }
    
    location /media/ {
        alias /path/to/new_tdl_site/media/;
        expires 30d;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Настройки продакшена в Django

В `settings.py` для продакшена:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
STATIC_ROOT = '/path/to/static/'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Приложения проекта

### 🛒 Cart (Корзина)
- Сессионная корзина товаров
- Оформление заказов с формами
- Email-уведомления
- reCAPTCHA защита

**Ключевые модели:**
- `Cart` - корзина покупок
- `Order` - заказы клиентов
- `OrderItem` - товары в заказе

### 📦 Good (Товары)
- Каталог товаров с категориями
- Мультигородность
- SEO-оптимизация
- Фильтрация и поиск

**Ключевые модели:**
- `Product` - товары
- `Category` - категории (с вложенностью)
- `City` - города для доставки

### 📝 Blog (Блог)
- Система статей с категориями
- Теги и фильтрация
- SEO-мета данные
- Подсчет просмотров

**Ключевые модели:**
- `Post` - статьи блога
- `Category` - категории блога
- `Tag` - теги

### 📞 Leads (Лиды и CRM)
- Система заявок
- Telegram-интеграция
- Управление менеджерами
- Автоматические уведомления

**Ключевые модели:**
- `Call` - заявки/звонки
- `Manager` - менеджеры
- `Result` - статусы заявок

### 🏠 Commonpages (Основные страницы)
- Главная страница
- Статические страницы
- Формы обратной связи
- Калькуляторы

## 🤖 API для Telegram-бота

Проект включает REST API для интеграции с внешним Telegram-ботом:

### Эндпоинты заявок
```
GET/POST /api/v1/callslist/           # Список заявок
GET      /api/v1/callslist/{id}/      # Детали заявки
PUT      /api/v1/callslist/{id}/      # Обновление заявки
GET      /api/v1/callslist/manager-tg/{tg_id}/  # Заявки менеджера
```

### Аутентификация
API защищен токенами через middleware:
```python
Authorization: YOUR_API_TOKEN
```

## 🔄 Celery задачи

### Автоматические уведомления
- **Ежедневная проверка** истекающих заявок (12:00)
- **Email-рассылка** при создании заказов
- **Telegram-уведомления** менеджерам

### Настройка планировщика
```python
app.conf.beat_schedule = {
    'check-notifications-every-day': {
        'task': 'leads.tasks.check_notifications',
        'schedule': crontab(hour='12', minute='00'),
    },
}
```

## 🎨 Frontend особенности

### Адаптивный дизайн
- Мобильная оптимизация для всех страниц
- Touch-интерфейсы для мобильных устройств
- Прогрессивное улучшение (Progressive Enhancement)

### JavaScript функциональность
- **AJAX-корзина** без перезагрузки страниц
- **Модальные окна** для форм
- **Яндекс.Карты** интеграция
- **Калькуляторы** стоимости

### SEO и производительность
- **Lazy loading** изображений
- **Минификация** CSS/JS
- **Gzip сжатие** статики
- **CDN-ready** структура

## 🔍 SEO оптимизация

### Sitemap и роботы
- Автоматическая генерация sitemap.xml
- Поддержка изображений в sitemap
- Настроенный robots.txt
- Канонические URL

### Микроразметка
- Schema.org для товаров
- Breadcrumbs навигация
- Организационная разметка
- FAQ разметка

### Метатеги
- Динамические title/description
- Open Graph теги
- Twitter Cards
- Structured Data

## 🛡️ Безопасность

### Защита форм
- **reCAPTCHA v3** для всех форм
- **Honeypot** поля против ботов
- **CSRF** защита Django
- **Rate limiting** (настраивается)

### Данные
- **Валидация** на уровне модели
- **Санитизация** пользовательского ввода
- **Логирование** ошибок безопасности

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test cart

# С покрытием кода
coverage run --source='.' manage.py test
coverage report
```

### Структура тестов
```
app_name/
├── tests/
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_api.py
```

## 📈 Мониторинг и логирование

### Логи
- **Django logs** - application.log
- **Nginx logs** - access.log, error.log
- **Celery logs** - celery_worker.log

### Мониторинг
- **Яндекс.Метрика** - веб-аналитика
- **Email alerts** - критические ошибки
- **Telegram alerts** - системные уведомления

## 🤝 Разработка

### Git Workflow
```bash
# Создание feature ветки
git checkout -b feature/new-feature

# Коммит изменений
git add .
git commit -m "feat: добавлена новая функция"

# Push и создание PR
git push origin feature/new-feature
```

### Code Style
- **PEP 8** для Python
- **Black** форматтер
- **isort** для импортов
- **flake8** линтер

### Полезные команды
```bash
# Создание приложения
python manage.py startapp app_name

# Создание миграций
python manage.py makemigrations

# Shell с Django контекстом
python manage.py shell

# Экспорт данных
python manage.py dumpdata app.Model > fixture.json

# Сбор статики
python manage.py collectstatic
```

## 🔧 Устранение неполадок

### Частые проблемы

1. **Ошибки миграций:**
```bash
python manage.py migrate --fake-initial
```

2. **Проблемы с Redis:**
```bash
redis-cli ping  # Проверка соединения
```

3. **Celery не работает:**
```bash
celery -A new_tdl_site inspect active
```

4. **Статика не загружается:**
```bash
python manage.py collectstatic --clear
```

### Логи для диагностики
```bash
# Django логи
tail -f logs/django.log

# Nginx логи
tail -f /var/log/nginx/access.log

# Celery логи
tail -f logs/celery.log
```

## 📚 Документация

### Дополнительные ресурсы
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Архитектурные решения
Подробная техническая документация доступна в файле [`README.md`](README.md) в корне проекта.

## 🤝 Contributing

1. Создайте feature branch (`git checkout -b feature/amazing-feature`)
2. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
3. Отправьте в branch (`git push origin feature/amazing-feature`)
4. Создайте Pull Request

## 📄 Лицензия

Этот проект является собственностью ООО "ТД Ленинградский". Все права защищены.

## 👥 Команда

- **Архитектор проекта:** Разработчик Django
- **Frontend разработчик:** Специалист по адаптивной верстке
- **DevOps инженер:** Настройка серверов и развертывание

## 📞 Поддержка

Для вопросов по разработке:
- **Email:** tech@tdleningrad.ru  
- **Telegram:** @tdleningradsky
- **Phone:** +7 (949) 624-2644

---

**ТД Ленинградский** - надежные строительные материалы для вашего успеха! 🏗️