from .models import RemovedCategory
from rest_framework import serializers


class RemovedCtgrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RemovedCategory
        fields = ('name', )