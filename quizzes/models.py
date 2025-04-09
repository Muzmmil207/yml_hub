from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from courses.models import Lesson


class Quiz(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quizzes",
        help_text="Select the lesson this quiz belongs to.",
        verbose_name="Lesson",
    )
    title = models.CharField(
        max_length=255,
        help_text="Enter the quiz title (max 255 characters).",
        verbose_name="Quiz Title",
    )
    description = CKEditor5Field(
        blank=True,
        null=True,
        help_text="Provide a brief description of the quiz (optional).",
        verbose_name="Quiz Description",
    )
    answer = models.CharField(max_length=255, help_text="The quiz answer")

    def __str__(self):
        return f"Quiz: {self.title} (Lesson: {self.lesson.title})"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.student.username} - {self.quiz.title} (Correct: {self.is_correct})"
        )
