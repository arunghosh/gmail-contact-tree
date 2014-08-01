from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MailSerializer
from contact.models import UserContact


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