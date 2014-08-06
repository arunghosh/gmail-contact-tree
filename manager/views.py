from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from Levenshtein import ratio
from common.views import JSONResponseMixin
from django.views.generic.base import View
import json
from .serializer import ContactZoneSerializer, MyUserSerializer, DuplicateContactSerializer
from zone import ByZoneMgr
from contact.models import UserContact
from django.db import transaction
from .merge import Merge
from contact import ContactStatus

@login_required(login_url='/login')
def home(request):
    return render(request, 'inbox_home.html')


class ContactsWithZoneView(APIView):

    def get(self, request):
        user = request.user
        manager = ByZoneMgr(user)
        slz = ContactZoneSerializer(manager.contacts_with_zone, many=True)
        return Response(slz.data)


class UserInfo(APIView):

    def get(self, request):
        user = request.user
        slz = MyUserSerializer(user)
        return Response(slz.data)


class DuplicateContacts(APIView):

    def get(self, request, cid):
        user = request.user
        c = UserContact.objects.get(pk=cid)
        name = c.name.lower()
        contacts = [ln for ln in ContactStatus.get_active(user) if ratio(name, ln.name.lower()) > .76 and c.id != ln.id]
        slz = DuplicateContactSerializer(contacts, many=True)
        return Response(slz.data)


class MergeContacts(APIView):

    @transaction.atomic
    def post(self, request):
        data = json.loads(request.read())
        merge = Merge(data['org_id'], data['dup_id'])
        merge.execute()
        manager = ByZoneMgr(request.user)
        contact = manager.get_contact_with_zone(merge.org)
        slz = ContactZoneSerializer(contact)
        return Response(slz.data)
