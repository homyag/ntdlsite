from rest_framework import serializers

from leads.models import Call, Result, Manager


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        # здесь можно указать конкретные поля модели, которые будут выводиться
        # пользователю
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class CallCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['comment']


class CallResultUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['result']


class CallManagerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['manager']
