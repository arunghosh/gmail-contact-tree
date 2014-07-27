from rest_framework import serializers
from contact.models import UserContact


class ContactSerializer(serializers.ModelSerializer):

    zone = serializers.IntegerField(default=0)
    email = serializers.SerializerMethodField('get_email')

    class Meta:
        model = UserContact
        fields = ('name', 'id', 'zone', 'status', 'email', 'category')

    def get_email(self, obj):
        return obj.mailcontact_set.all()[0].email

# class ByZoneSerializer(serializers.Serializer):
#
#     safe = ContactSerializer(many=True)
#     unsafe = ContactSerializer(many=True)
#     inter = ContactSerializer(many=True)
#
#
# class DateContactMapSerializer(serializers.Serializer):
#
#     contacts = ContactSerializer(many=True)
#     date = serializers.DateField()

    # class Meta:
    #     model = DateContactMap
    #     fields = ('date', 'contacts',)