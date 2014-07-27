from django.shortcuts import render


def login(request):
    return render(request, "auth_login.html", {})


