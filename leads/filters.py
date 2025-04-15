from django_filters import rest_framework as filters
from leads.models import Call


class CallFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created', lookup_expr='lte')
    manager_tg_id = filters.NumberFilter(field_name='manager__tg_id')
    exclude_result_ids = filters.BaseInFilter(field_name='result_id',
                                              exclude=True)

    class Meta:
        model = Call
        fields = ['created', 'start_date', 'end_date', 'manager_tg_id']

    @property
    def qs(self):
        parent = super().qs
        exclude_ids = [2, 3, 5, 7, 8, 9, 12]
        return parent.exclude(result_id__in=exclude_ids)
