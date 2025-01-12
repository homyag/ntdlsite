import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_tdl_site.settings')
app = Celery('new_tdl_site')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в каждом установленном приложении Django
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-notifications-every-day': {
        'task': 'leads.tasks.check_notifications',
        'schedule': crontab(hour='12', minute='00'),
    },
}