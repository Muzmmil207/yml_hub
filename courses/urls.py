from django.urls import path

from . import api

urlpatterns = [
    path("get-courses", api.get_courses),
]
