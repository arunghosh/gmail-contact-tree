from rest_framework import serializers
from django.conf import settings
from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(format=settings.TIME_FORMAT)
    name = serializers.SerializerMethodField('get_name')
    cid = serializers.SerializerMethodField('get_cid')

    class Meta:
        model = Reminder
        fields = ('id', 'remark', 'date', 'name', 'cid')

    def get_name(self, obj):
        return obj.contact.name

    def get_cid(self, obj):
        return obj.contact.id