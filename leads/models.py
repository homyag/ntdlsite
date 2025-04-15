from datetime import datetime, timedelta

from django.db import models
from django.db.models import ForeignKey


class Result(models.Model):
    name = models.CharField(max_length=50, verbose_name='Результат')

    class Meta:
        db_table: str = 'result'
        verbose_name: str = 'Результат'
        verbose_name_plural: str = 'Результаты'

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=50, verbose_name='Менеджер', null=True,
                            blank=True)
    mail = models.EmailField(verbose_name='Электронная почта менеджера',
                             null=True, blank=True)
    tg_id = models.BigIntegerField(verbose_name='ID в Телеграм', null=True,
                                   blank=True)

    class Meta:
        db_table: str = 'manager'
        verbose_name: str = 'Менеджер'
        verbose_name_plural: str = 'Менеджеры'

    def __str__(self):
        return self.name


class Call(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name='Дата звонка')
    resource = models.CharField(max_length=50, verbose_name='Источник',
                                null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона',
                             null=True, blank=True)
    mail = models.EmailField(verbose_name='Электронная почта', null=True,
                             blank=True)
    name = models.CharField(max_length=50, verbose_name='Организация/ЧЛ',
                            null=True, blank=True)
    result = ForeignKey(to=Result, on_delete=models.CASCADE,
                        verbose_name='Результат')
    comment = models.TextField(blank=True, null=True,
                               verbose_name='Комментарий')
    manager = models.ForeignKey(to=Manager, on_delete=models.CASCADE,
                                verbose_name='Менеджер')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Последнее обновление')

    date_of_notification = models.DateField(null=True, blank=True,
                                            verbose_name='Дата уведомления')

    class Meta:
        db_table: str = 'call'
        verbose_name: str = 'Звонок'
        verbose_name_plural: str = 'Звонки'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None

        # Если это существующая запись, получаем оригинальный экземпляр из базы данных
        if not is_new_instance:
            original = Call.objects.get(pk=self.pk)
        else:
            original = None

        # Проверяем изменения поля result и устанавливаем date_of_notification
        if is_new_instance or (original and original.result != self.result):
            # Добавление записи в комментарий
            change_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result_change_message = (f"\n[{change_date}] изменен результат:"
                                     f" {self.result.name}\n")

            if self.comment:
                self.comment += result_change_message
            else:
                self.comment = result_change_message

            # Установка даты уведомления на основе значения result
            if self.result.name == "в работе" and not self.date_of_notification:
                self.date_of_notification = datetime.now().date() + timedelta(
                    days=3)
            elif self.result.name == "ожидание ответа от клиента":
                self.date_of_notification = datetime.now().date() + timedelta(
                    days=1)
            elif self.result.name == "отправлено КП":
                self.date_of_notification = datetime.now().date() + timedelta(
                    days=3)
            elif self.result.name == "отправлено сообщение":
                self.date_of_notification = datetime.now().date() + timedelta(
                    days=3)
            elif self.result.name == "отправлен договор":
                self.date_of_notification = datetime.now().date() + timedelta(
                    days=7)
            else:
                self.date_of_notification = None

        super().save(*args, **kwargs)


class Good(models.Model):
    category = models.CharField(max_length=50, verbose_name='Категория')
    name = models.CharField(max_length=50, verbose_name='Наименование')
    article = models.CharField(max_length=50, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')

    class Meta:
        db_table: str = 'product'
        verbose_name: str = 'Товар'
        verbose_name_plural: str = 'Товары'

    def __str__(self):
        return self.name


class CallItem(models.Model):
    call = models.ForeignKey(to=Call, on_delete=models.CASCADE,
                             verbose_name='Звонок')
    good = models.ForeignKey(to=Good, on_delete=models.CASCADE,
                             verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.call.name

    def get_cost(self):
        return self.price * self.quantity
