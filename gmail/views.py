from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import Auth
from django.http import HttpResponseRedirect
from auth.models import MyUser
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from .parsers import InboxImport


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
    # in_import = InboxImport(user)
    # in_import.import_all()
    return HttpResponseRedirect('/')



# @login_required()
# def initial_import(request):
#     user = request.user
#     in_import = InboxImport(user)
#     in_import.import_all()
#     return render(request, "inbox_home.html")
#
#
