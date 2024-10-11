from rest_framework import generics
from rest_framework.exceptions import NotFound

from leads.filters import CallFilter
from leads.models import Call, Manager, Result
from leads.serializers import CallSerializer, CallCommentUpdateSerializer, \
    ManagerSerializer, CallResultUpdateSerializer, ResultSerializer, \
    CallManagerUpdateSerializer

from rest_framework.views import APIView

from django_filters import rest_framework as filters


# получает весь список заявок по GET запросу api/v1/callslist/ и может
# добавлять новую заявку по POST запросу
class CallsApiList(generics.ListCreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


# получает весь список менеджеров по GET запросу api/v1/managers/ и может
# добавлять нового менеджера по POST запросу
class ManagersApiList(generics.ListCreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


# получает весь список результатов по GET запросу api/v1/results/ и может
# добавлять новые резудьтаты по POST запросу
class ResultsApiList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


# обновляет одну заявку api/v1/callslist/<int:pk>/
class CallsApiUpdate(generics.UpdateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


# получает одну заявку по id api/v1/callslist/call/<int:pk>/
class CallsDetailView(generics.RetrieveAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def get_object(self):
        object = super().get_object()
        if object is None:
            raise NotFound('Звонок не найден')
        return object


# получает список заявок по id менеджера api/v1/callslist/manager-tg/<int:tg_id>/
class CallsByManagerTgIdApiList(generics.ListCreateAPIView):
    serializer_class = CallSerializer

    def get_queryset(self):
        tg_id = self.kwargs['tg_id']
        return Call.objects.filter(manager__tg_id=tg_id)


# обновляет заявку по id менеджера и id заявки api/v1/callslist/manager-tg/<int:tg_id>/<int:pk>/
class CallsByManagerTgIdApiUpdate(generics.UpdateAPIView):
    serializer_class = CallSerializer

    def get_queryset(self):
        tg_id = self.kwargs['tg_id']
        return Call.objects.filter(manager__tg_id=tg_id)


# получает список заявок в диапазоне дат по id менеджера
# /api/v1/callsist/filter/?manager_tg_id={tg_id}&start_date={
# start_date}&end_date={end_date}
class CallByManagerTgIdAndDateRangeApiList(generics.ListAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CallFilter


# обновляет комментарий заявки по id заявки api/v1/calllist/partial_update/<int:pk>/
class CallCommentUpdateView(generics.UpdateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallCommentUpdateSerializer
    http_method_names = ['put', 'patch']


class CallResultUpdateView(generics.UpdateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallResultUpdateSerializer
    http_method_names = ['put', 'patch']


class CallManagerUpdateView(generics.UpdateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallManagerUpdateSerializer
    http_method_names = ['put', 'patch']
