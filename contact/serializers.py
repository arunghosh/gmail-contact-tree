from rest_framework import serializers
from django.conf import settings
from . import CommItem


class CommItemSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format=settings.TIME_FORMAT)
    remark = serializers.CharField()
    type = serializers.IntegerField()
    direction = serializers.IntegerField()
    mail_id = serializers.CharField()

class CommStaterializer(serializers.Serializer):
    month = serializers.CharField()
    mail_count = serializers.IntegerField()
    call_count = serializers.IntegerField()
