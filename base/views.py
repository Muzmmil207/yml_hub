from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

def landing_page(request: HttpRequest):
    return render(request, "base/landing-page.html")


@login_required
def dashboard_view(request: HttpRequest):
    return render(request, "base/dashboard.html")


@login_required
def courses_view(request: HttpRequest):
    return render(request, "base/courses.html")
