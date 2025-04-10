from django.urls import path

from .views import (
    course_view,
    courses_view,
    dashboard_view,
    landing_page,
    lesson_view,
    profile_view,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("courses/", courses_view, name="courses"),
    path("courses/<slug:course_slug>/~/<int:course_id>", course_view, name="course"),
    path("<slug:course_title>/lesson/<int:lesson_id>/", lesson_view, name="lesson"),
]
