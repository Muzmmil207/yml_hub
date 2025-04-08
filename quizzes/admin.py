from django.contrib import admin

from .models import Answer, Quiz, QuizAttempt


class AnswerInline(admin.TabularInline):  # Allows inline answer creation in Quiz admin
    model = Answer
    extra = 2  # Default empty answer fields to add quickly


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson")  # Display key fields in admin list
    search_fields = ("title", "lesson__title")  # Search by quiz and lesson title
    list_filter = ("lesson",)  # Filter quizzes by lesson
    inlines = [AnswerInline]  # Allow adding answers directly in quiz admin


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")  # Show answer details


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "quiz",
        "answered_at",
    )
    search_fields = ("student__username", "quiz__title")
