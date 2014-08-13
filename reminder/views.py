from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from common.views import JSONResponseMixin
from contact.models import UserContact
from django.views.generic.base import View
from .serializers import ReminderSerializer
from . import ReminderStatus, get_active_reminders
import json

from .models import Reminder


class AddReminder(APIView):

    def post(self, request):
        data = json.loads(request.read())
        cid = data['cid']
        date = data['date']
        remark = data['remark']
        reminder = Reminder()
        reminder.contact = UserContact.objects.get(pk=cid)
        reminder.date = datetime.strptime(date, "%Y-%m-%d")
        reminder.remark = remark
        reminder.status = ReminderStatus.active
        reminder.save()
        return Response(ReminderSerializer(reminder).data)


class DeleteReminder(JSONResponseMixin, View):

    def post(self, request):
        data = json.loads(request.read())
        reminder = Reminder.objects.get(pk=int(data['id']))
        print ReminderStatus.inactive
        reminder.status = ReminderStatus.inactive
        reminder.save()
        return self.render_json_response({'status': True})


class Reminders(APIView):

    def get(self, request, cid):
        return Response(get_active_reminders(cid))


class AllReminders(APIView):

    def get(self, request):
        user = request.user
        reminders = [r for c in user.usercontact_set.all() for r in c.reminder_set.all() if r.status == ReminderStatus.active]
        slz = ReminderSerializer(reminders, many=True)
        return Response(slz.data)


