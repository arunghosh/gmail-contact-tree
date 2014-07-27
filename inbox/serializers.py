from rest_framework import serializers
from .models import UserContact, MailMessage

class ContactSerializer(serializers.ModelSerializer):

    zone = serializers.IntegerField(default=0)

    class Meta:
        model = UserContact
        fields = ('name', 'id', 'zone', 'status')


class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailMessage
        fields = ('message_id','subject', 'date', 'folder',)