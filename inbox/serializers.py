from rest_framework import serializers
from .models import UserContact, MailMessage
from contact import MailDirection

# class ContactSerializer(serializers.ModelSerializer):
#
#     zone = serializers.IntegerField(default=0)
#
#     class Meta:
#         model = UserContact
#         fields = ('name', 'id', 'zone', 'status')


class MailSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = MailMessage
        fields = ('message_id','subject', 'date', 'folder', 'name')

    def get_name(self, obj):
        contacts = obj.mailcontactmap_set.filter(type=MailDirection.FROM)
        if len(contacts) > 0:
            return contacts[0].mail_contact.user_contact.name
        else:
            return "self"

