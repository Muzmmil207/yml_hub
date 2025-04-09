from django.contrib import admin

from .models import Quiz, QuizAttempt


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson")  # Display key fields in admin list
    search_fields = ("title", "lesson__title")  # Search by quiz and lesson title
    list_filter = ("lesson",)  # Filter quizzes by lesson


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "quiz",
        "answered_at",
    )
    search_fields = ("student__username", "quiz__title")
