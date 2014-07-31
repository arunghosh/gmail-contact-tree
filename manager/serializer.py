from rest_framework import serializers
from contact.models import UserContact
from auth.models import MyUser

class ContactSerializer(serializers.ModelSerializer):

    zone = serializers.IntegerField(default=0)
    email = serializers.SerializerMethodField('get_email')
    mobile = serializers.SerializerMethodField('get_mobile')
    delta = serializers.IntegerField()

    class Meta:
        model = UserContact
        fields = ('name', 'id', 'zone', 'status', 'email', 'category', 'mobile', 'delta')

    def get_email(self, obj):
        if len(obj.mailcontact_set.all()) > 0:
            return obj.mailcontact_set.all()[0].email
        else:
            return "--"

    def get_mobile(self, obj):
        if len(obj.mobilecontact_set.all()) > 0:
            return obj.mobilecontact_set.all()[0].number
        else:
            return "--"

class MyUserSerializer(serializers.ModelSerializer):

    ln_count = serializers.SerializerMethodField('get_ln_count')

    class Meta:
        model = MyUser
        fields = ('name','email', 'phone', 'ln_count')

    def get_ln_count(self, obj):
        return len(obj.lncontact_set.all())
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