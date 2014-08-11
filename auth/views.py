from django.shortcuts import render
from django.contrib.auth import logout


def login(request):
    return render(request, "auth_login.html", {})


def logout(request):
    logout(request)
    return render(request, "auth_login.html", {})