from rest_framework import serializers
from .models import LnContact


class LnContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = LnContact
        fields = ('id', 'name', 'headline', 'image_url', 'profile_url')
