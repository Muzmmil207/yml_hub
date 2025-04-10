from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Enrollment, Lesson, LessonProgress
from users.models import CustomUser

from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSubmissionSerializer


@api_view(["GET"])
def get_courses(request):
    courses = Course.objects.filter(status="Active")
    data = []

    for course in courses:
        instructor: CustomUser = course.instructor
        lessons: list[Lesson] = course.lessons.all()

        learning_points = [
            learning_point.strip()
            for learning_point in course.learning_points.split(";")
            if len(learning_point) > 1
        ]

        course_data = {
            "id": course.id,
            "title": course.title,
            "category": course.category.name if course.category else "Uncategorized",
            "description": course.description,
            "instructor": {
                "name": instructor.get_full_name() or instructor.username,
                "image": instructor.userprofile.avatar_url,
            },
            "image": course.thumbnail_url,
            "duration": course.get_duration_display() if course.duration else "N/A",
            "level": course.get_level_display(),
            "students": f"{course.enrollment_set.count()}",
            "language": course.language,
            "rating": (
                f"{course.rating} ({course.review_count})"
                if hasattr(course, "rating")
                else "No ratings"
            ),
            "learningPoints": learning_points,
            "lessons": [
                {
                    "title": lesson.title,
                    "duration": lesson.get_duration_display(),
                }
                for lesson in lessons
            ],
        }

        data.append(course_data)

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enroll_in_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(student=user, course=course)

    if not created:
        # Already enrolled, get the last accessed lesson
        progress = LessonProgress.objects.filter(
            student=user, lesson__course=course
        ).latest("id")
        if progress:
            return redirect(
                f"/{slugify(course.title,allow_unicode=True)}/lesson/{progress.lesson.id}/"
            )

    # New enrollment or no previous progress, redirect to first lesson
    first_lesson = Lesson.objects.filter(course=course).earliest("created_at")
    if first_lesson:
        return redirect(
            f"/{slugify(course.title,allow_unicode=True)}/lesson/{first_lesson.id}/"
        )
    else:
        return Response({"detail": "No lessons found in this course."}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_lesson_as_complete(request, lesson_id):
    user = request.user

    try:
        lesson_progress = LessonProgress.objects.get(lesson__id=lesson_id, student=user)
        lesson_progress.completed = True
        lesson_progress.save()
        return Response({}, status=200)
    except:
        pass

    return Response({"detail": "No lessons found in this course."}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_assignment(request):
    serializer = AssignmentSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        assignment = serializer.validated_data["assignment"]
        student = request.user

        # Prevent duplicate submission
        if AssignmentSubmission.objects.filter(
            assignment=assignment, student=student
        ).exists():
            return Response(
                {"message": "You have already submitted this assignment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        AssignmentSubmission.objects.create(
            assignment=assignment,
            student=student,
            attachment=serializer.validated_data.get("attachment"),
        )
        return Response(
            {
                "message": "Assignment submitted successfully. You will be notified once it's reviewed."
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
