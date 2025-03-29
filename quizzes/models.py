from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

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
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Provide a brief description of the quiz (optional).",
        verbose_name="Quiz Description",
    )
    max_score = models.PositiveIntegerField(
        default=100,
        help_text="Set the maximum score a student can achieve in this quiz.",
        verbose_name="Maximum Score",
    )

    def __str__(self):
        return f"Quiz: {self.title} (Lesson: {self.lesson.title})"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = RichTextField()
    question_type = models.CharField(
        max_length=10,
        choices=[("MCQ", "Multiple Choice"), ("TEXT", "Text Input")],
        default="MCQ",
    )

    def __str__(self):
        return f"Question: {self.text} (Quiz: {self.quiz.title})"


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text} (Correct: {self.is_correct})"


class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} (Score: {self.score})"
