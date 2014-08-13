from django.shortcuts import render
from auth.models import MyUser
from rest_framework.views import APIView
from rest_framework.response import Response
from common.views import JSONResponseMixin
from django.views.decorators.csrf import csrf_exempt
from .parsers import ImportMobile
import json
from django.db import transaction
from contact.models import UserContact

from .serializer import MobileCallSerializer

class UpdateCallsView(JSONResponseMixin, APIView):

    @csrf_exempt
    @transaction.atomic
    def post(self, request):
        try:
            ImportMobile(request)
            return self.render_json_response({'status': 'true'})
        except Exception, e:
            print "************Error"
            print str(e)
            return self.render_json_response({'status': 'false'})


class GetUserIdForMobView(JSONResponseMixin, APIView):

    def get(self, request, phone):
        try:
            user = MyUser.objects.get(phone=phone)
            return self.render_json_response({'status': 'true', 'id': user.id})
        except:
            return self.render_json_response({'status': 'false'})


class RecentCallsView(APIView):

    def get(self, request):
        user = request.user
        calls = list(user.mobilecall_set.all())
        calls.sort(key=lambda x: x.date, reverse=True)
        slz = MobileCallSerializer(calls[0:20], many=True)
        return Response(slz.data)


class CallListView(APIView):

    def get(self, request, cid):
        contact = UserContact.objects.get(pk=cid)
        calls = contact.calls
        slz =MobileCallSerializer(calls, many=True)
        return Response(slz.data)
