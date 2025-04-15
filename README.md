# Напоминалка для себя

библиотека *openpyxl* - установлена для передачи данных из модели в эксель

## Celery

Запуск сервера redis
```shell
redis-server
```
Запуск вокера celery
```shell
celery -A new_tdl_site worker --loglevel=info
```
Запуск celery-beat
```shell
celery -A new_tdl_site worker --beat
```