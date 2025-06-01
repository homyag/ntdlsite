from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
import re

from good.models import Tag, Product
from good.tag_data import CONCRETE_TAGS, TAG_PRODUCT_MAPPING


class Command(BaseCommand):
    help = 'Создает теги для гранитного бетона и назначает их товарам'

    def add_arguments(self, parser):
        parser.add_argument(
            '--assign-to-products',
            action='store_true',
            help='Назначить теги существующим товарам автоматически',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать какие товары будут затронуты без реального назначения тегов',
        )

    def handle(self, *args, **options):
        created_tags = 0
        updated_tags = 0
        assigned_products = 0

        with transaction.atomic():
            # Создаем или обновляем теги
            for tag_data in CONCRETE_TAGS:
                tag, created = Tag.objects.get_or_create(
                    slug=tag_data['slug'],
                    defaults=tag_data
                )

                if created:
                    created_tags += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Создан тег: {tag.name}')
                    )
                else:
                    # Обновляем существующий тег
                    for field, value in tag_data.items():
                        if field != 'slug':  # slug не обновляем
                            setattr(tag, field, value)
                    tag.save()
                    updated_tags += 1
                    self.stdout.write(
                        self.style.WARNING(f'Обновлен тег: {tag.name}')
                    )

            # Назначаем теги товарам, если указан флаг
            if options['assign_to_products']:
                self.stdout.write('Назначение тегов товарам...')

                for tag_slug, grade_patterns in TAG_PRODUCT_MAPPING.items():
                    try:
                        tag = Tag.objects.get(slug=tag_slug)
                        self.stdout.write(f'\nОбработка тега: {tag.name}')

                        # Находим товары, которые соответствуют маркам для этого тега
                        for grade_pattern in grade_patterns:
                            # Используем более гибкий поиск
                            products = Product.objects.filter(
                                Q(name__iregex=rf'\b{re.escape(grade_pattern)}\b') & (
                                        Q(name__icontains='бетон') |
                                        Q(name__icontains='Бетон') |
                                        Q(name__icontains='БЕТОН') |
                                        Q(category__name__icontains='бетон')  # Также проверяем категорию
                                )
                            )

                            if options['dry_run']:
                                # Режим dry-run - только показываем что будет сделано
                                for product in products:
                                    if not product.tags.filter(id=tag.id).exists():
                                        self.stdout.write(
                                            f'  [DRY-RUN] Тег "{tag.name}" будет назначен товару "{product.name}"'
                                        )
                                        assigned_products += 1
                            else:
                                # Реальное назначение тегов
                                for product in products:
                                    # Проверяем, что товар еще не имеет этого тега
                                    if not product.tags.filter(id=tag.id).exists():
                                        product.tags.add(tag)
                                        assigned_products += 1
                                        self.stdout.write(
                                            f'  ✓ Тег "{tag.name}" назначен товару "{product.name}"'
                                        )

                        # Показываем статистику для каждого тега
                        if not options['dry_run']:
                            tag_products_count = Product.objects.filter(tags=tag).count()
                            if tag_products_count == 0:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'⚠ Внимание: для тега "{tag.name}" не найдено подходящих товаров'
                                    )
                                )
                            else:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'✓ Тег "{tag.name}" назначен {tag_products_count} товарам'
                                    )
                                )

                    except Tag.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Тег с slug "{tag_slug}" не найден')
                        )

        # Итоговая статистика
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'📊 ИТОГОВАЯ СТАТИСТИКА:'))
        self.stdout.write(f'  Создано тегов: {created_tags}')
        self.stdout.write(f'  Обновлено тегов: {updated_tags}')

        if options['assign_to_products']:
            action_text = "Будет назначено" if options['dry_run'] else "Назначено"
            self.stdout.write(f'  {action_text} тегов товарам: {assigned_products}')

        self.stdout.write('=' * 60)

        if not options['assign_to_products']:
            self.stdout.write(
                self.style.NOTICE(
                    '\n💡 Для автоматического назначения тегов товарам запустите команду с флагом --assign-to-products'
                )
            )
            self.stdout.write(
                self.style.NOTICE(
                    '💡 Для предварительного просмотра используйте флаг --dry-run'
                )
            )
        elif options['dry_run']:
            self.stdout.write(
                self.style.NOTICE(
                    '\n💡 Это был режим предварительного просмотра. Уберите флаг --dry-run для реального назначения тегов.'
                )
            )