from django.urls import path

from . import api

urlpatterns = [
    path("api/submit-quiz-answers", api.submit_quiz_answers),
]
