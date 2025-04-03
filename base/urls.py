from django.urls import path

from .views import courses_view, dashboard_view, landing_page

urlpatterns = [
    path("", landing_page, name="landing"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("courses/", courses_view, name="courses"),
]
