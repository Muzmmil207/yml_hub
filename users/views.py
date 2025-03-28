from django.http import HttpRequest
from django.shortcuts import render


def login_view(request: HttpRequest):

    return render(request, "login.html")
