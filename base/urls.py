from django.urls import path

from .views import (
    course_view,
    courses_view,
    dashboard_view,
    landing_page,
    lesson_view,
    parent_dashboard,
    profile_view,
    student_dashboard,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("courses/", courses_view, name="courses"),
    path("courses/<slug:course_slug>/~/<int:course_id>", course_view, name="course"),
    path("<slug:course_title>/lesson/<int:lesson_id>/", lesson_view, name="lesson"),
    path("dashboard/student/", student_dashboard, name="student-dashboard"),
    path("dashboard/parent/", parent_dashboard, name="parent-dashboard"),
]
