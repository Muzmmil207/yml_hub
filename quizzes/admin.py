from django.contrib import admin

from .models import Answer, Question, Quiz, QuizAttempt


class AnswerInline(
    admin.TabularInline
):  # Allows inline answer creation in Question admin
    model = Answer
    extra = 2  # Default empty answer fields to add quickly


class QuestionInline(
    admin.TabularInline
):  # Allows inline question creation in Quiz admin
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "max_score")  # Display key fields in admin list
    search_fields = ("title", "lesson__title")  # Search by quiz and lesson title
    list_filter = ("lesson",)  # Filter quizzes by lesson
    inlines = [QuestionInline]  # Allow adding questions directly in quiz admin


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "question_type")  # Display key fields
    list_filter = ("quiz", "question_type")  # Filter by quiz and type
    search_fields = ("text",)  # Enable search by question text
    inlines = [AnswerInline]  # Allow adding answers directly in question admin


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")  # Show answer details
    list_filter = ("is_correct",)  # Filter by correct/incorrect answers


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "quiz",
        "score",
        "completed",
        "started_at",
        "completed_at",
    )
    list_filter = ("completed",)
    search_fields = ("student__username", "quiz__title")
