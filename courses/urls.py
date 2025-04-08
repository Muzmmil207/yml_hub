from django.urls import path

from . import api

urlpatterns = [
    path("api/get-courses", api.get_courses),
    path("api/enroll/<int:course_id>", api.enroll_in_course),
    path("api/mark-lesson-as-complete/<int:lesson_id>", api.mark_lesson_as_complete),
]
