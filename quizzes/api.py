from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz, QuizAttempt


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_quiz_answers(request):
    student = request.user
    results = []

    for quiz_id, student_answer in request.data.items():
        if student_answer:
            try:
                quiz = Quiz.objects.get(pk=int(quiz_id))
                correct_answer = quiz.answer.strip().lower()
                submitted_answer = student_answer.strip().lower()
                is_correct = submitted_answer == correct_answer

                # Save the attempt
                try:
                    quiz_attempt = QuizAttempt.objects.get(
                        student=student,
                        quiz=quiz,
                    )
                    quiz_attempt.answer = student_answer
                    quiz_attempt.is_correct = is_correct
                    quiz_attempt.save()
                except QuizAttempt.DoesNotExist:
                    QuizAttempt.objects.create(
                        student=student,
                        quiz=quiz,
                        answer=student_answer,
                        is_correct=is_correct,
                    )

                results.append(
                    {
                        "quiz_id": quiz.id,
                        "quiz_title": quiz.title,
                        "your_answer": student_answer,
                        "is_correct": is_correct,
                    }
                )

            except (Quiz.DoesNotExist, ValueError):
                continue  # Skip invalid quiz IDs or data

    return Response(
        {"message": "Quiz answers submitted successfully.", "results": results}
    )
