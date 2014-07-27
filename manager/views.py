from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.base import View
from gmail.parsers import InboxImport
from .serializer import ContactSerializer
from . import ByZoneMgr
from contact.models import UserContact
from common.views import JSONResponseMixin


@login_required(login_url='/login')
def home(request):
    return render(request, 'inbox_home.html')


class UpdateFollowStatus(JSONResponseMixin, View):

    def post(self, request, cid, status):
        c = UserContact.objects.get(pk=cid)
        c.status = status
        c.save()
        return self.render_json_response({})


class ContactsWithZoneView(APIView):

    def get(self, request):
        user = request.user
        manager = ByZoneMgr(user)
        slz = ContactSerializer(manager.update_zone(), many=True)
        return Response(slz.data)


class RefreshInboxView(APIView):

    @transaction.atomic
    def get(self, request):
        user = request.user
        in_import = InboxImport(user)
        result = in_import.import_new()
        return Response({'count': result.count})


class ImportInboxView(APIView):

    @transaction.atomic
    def get(self, request):
        user = request.user
        in_import = InboxImport(user)
        result = in_import.import_old()
        return Response({'count': result.count})


