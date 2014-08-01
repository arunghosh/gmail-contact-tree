from rest_framework import serializers
from contact.models import UserContact
from auth.models import MyUser


class DuplicateContactSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField('get_email')
    mobile = serializers.SerializerMethodField('get_mobile')

    class Meta:
        model = UserContact
        fields = ('name', 'id', 'status', 'email', 'category', 'mobile')

    def get_email(self, obj):
        if len(obj.mailcontact_set.all()) > 0:
            return ', '.join([mc.email for mc in obj.mailcontact_set.all()])
        else:
            return "--"

    def get_mobile(self, obj):
        if len(obj.mobilecontact_set.all()) > 0:
            return ', '.join([mc.number for mc in obj.mobilecontact_set.all()])
        else:
            return "--"


class ContactZoneSerializer(DuplicateContactSerializer):

    zone = serializers.IntegerField(default=0)
    delta = serializers.IntegerField()

    class Meta:
        model = UserContact
        fields = ('name', 'id', 'zone', 'status', 'email', 'category', 'mobile', 'delta')


class MyUserSerializer(serializers.ModelSerializer):

    ln_count = serializers.SerializerMethodField('get_ln_count')

    class Meta:
        model = MyUser
        fields = ('name', 'email', 'phone', 'ln_count')

    def get_ln_count(self, obj):
        return len(obj.lncontact_set.all())