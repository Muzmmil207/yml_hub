from django.http import HttpRequest
from django.shortcuts import  render


def landing_page(request: HttpRequest):
    return render(request, "base/landing-page.html")