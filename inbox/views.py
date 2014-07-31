from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gmail.parsers import InboxImport
from gmail import Auth
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactSerializer, MailSerializer
from .models import MailContact
from contact.models import UserContact


# class ContactsView(APIView):
#
#     def get(self, request):
#         user = request.user
#         contacts = user.usercontact_set.all()
#         contacts.sort(key=lambda x: x.last_contacted_on, reverse=True)
#         slz = ContactSerializer(contacts, many=True)
#         return Response(slz.data)


class MailListView(APIView):

    def get(self, request, cid):
        contact = UserContact.objects.get(pk=cid)
        mails = contact.mails
        slz = MailSerializer(mails, many=True)
        return Response(slz.data)


class RecentMailsView(APIView):

    def get(self, request):
        user = request.user
        mails = list(user.mailmessage_set.all())
        mails.sort(key=lambda x: x.date, reverse=True)
        slz = MailSerializer(mails[0:20], many=True)
        return Response(slz.data)