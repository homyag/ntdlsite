import openpyxl

from django.contrib import admin
from django.http import HttpResponse

from .models import Call, Result, Manager, CallItem, Good


class CallItemInline(admin.TabularInline):
    model = CallItem
    raw_id_fields = ['good']


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'resource', 'phone', 'name', 'result',
                    'manager', 'date_of_notification']
    list_filter = ['created', 'resource', 'updated', 'manager', 'result',
                   'date_of_notification']
    list_editable = ['resource', 'result', 'date_of_notification']
    list_per_page = 100
    search_fields = ['phone', 'mail', 'name', 'date_of_notification', 'comment']
    ordering = ['-created']
    inlines = [CallItemInline]
    actions = ['mark_as_done', 'mark_as_empty', 'export_calls_to_excel']

    @admin.action(description='Закрыть заявку (пустой звонок)')
    def mark_as_empty(self, request, queryset):
        queryset.update(result=Result.objects.get(pk=2))

    @admin.action(description='Закрыть заявку (произведена отправка)')
    def mark_as_done(self, request, queryset):
        queryset.update(result=Result.objects.get(pk=3))

    @admin.action(description='Экспорт в Excel')
    def export_calls_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Calls"

        columns = ['ID', 'Created', 'Resource', 'Phone', 'Name', 'Result',
                   'Manager',
                   'comment', 'date_of_notification']
        ws.append(columns)

        for call in queryset:
            row = [
                call.id,
                call.created,
                call.resource,
                call.phone,
                call.name,
                str(call.result),
                str(call.manager),
                call.comment,
                call.date_of_notification
            ]
            ws.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=calls.xlsx'
        wb.save(response)

        return response


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id''name']


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mail', 'tg_id']
    search_fields = ['name', 'mail', 'tg_id']


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'article', 'price']
    search_fields = ['category', 'name', 'article']