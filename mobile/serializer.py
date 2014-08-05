from rest_framework import serializers
from django.conf import settings
from .models import MobileCall


class MobileCallSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(format=settings.TIME_FORMAT)

    class Meta:
        model = MobileCall
        fields = ('date',)
