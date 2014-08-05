from django.shortcuts import render
from common.views import JSONResponseMixin
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from calendar import month_name
from datetime import datetime

from .serializers import CommItemSerializer, CommStaterializer
from .models import UserContact
from . import CommStat, CommItem


class UpdateFollowStatus(JSONResponseMixin, View):

    def post(self, request, cid, status):
        c = UserContact.objects.get(pk=cid)
        c.status = status
        c.save()
        return self.render_json_response({})


class UpdateMobile(JSONResponseMixin, View):

    def post(self, request, mobile):
        user = request.user
        user.phone = mobile
        print mobile
        user.save()
        return self.render_json_response({'status': True})


class UpdateCtgry(JSONResponseMixin, View):

    def post(self, request, cid, ctgry):
        c = UserContact.objects.get(pk=cid)
        c.category = ctgry
        c.save()
        return self.render_json_response({'status': True})


class CommItemsView(APIView):

    def get(self, request, cid):
        contact = UserContact.objects.get(pk=cid)
        mails = contact.all_communications
        slz = CommItemSerializer(mails[:40], many=True)
        return Response(slz.data)


class MonthView(APIView):

    def get(self, request, cid):
        contact = UserContact.objects.get(pk=cid)
        mails = contact.all_communications
        mail_result = {}
        call_result = {}
        for r in range(datetime.now().month - 6, datetime.now().month + 1):
            mail_result[r] = 0
            call_result[r] = 0

        for c in [m for m in mails if m.type == CommItem.mail]:
            month = c.date.month
            mail_result[month] = mail_result.get(month, 0) + 1

        for c in [m for m in mails if m.type != CommItem.mail]:
            month = c.date.month
            call_result[month] = call_result.get(month, 0) + 1

        result = [CommStat(month_name[int(i)][:3], mail_result[i], call_result[i], i) for i in mail_result]
        result.sort(key=lambda x: x.index)
        slz = CommStaterializer(result, many=True)
        return Response(slz.data)
