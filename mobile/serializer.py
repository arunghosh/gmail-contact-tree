from rest_framework import serializers
from .models import MobileCall


class MobileCallSerializer(serializers.ModelSerializer):

    class Meta:
        model = MobileCall
        fields = ('date',)
