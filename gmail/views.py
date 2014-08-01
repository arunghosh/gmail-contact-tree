from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from auth.models import MyUser
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from .parsers import InboxImport
from django.db import transaction
from . import Auth


def login(request):
    return HttpResponseRedirect(Auth.get_auth_url() + "&approval_prompt=force")


def callback(request):
    code = request.GET['code']
    user = Auth.get_user_and_update_cred(code)
    try:
        user = MyUser.objects.get(email=user.email)
        user.gmail_token = code
        user.save()
    except ObjectDoesNotExist:
        user = MyUser.objects.create_user(email=user.email, name=user.name, image_url=user.image_url, password='auto')
    user = authenticate(email=user.email, password='auto')
    auth_login(request, user)
    return HttpResponseRedirect('/')


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