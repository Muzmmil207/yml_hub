from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import (
    AssignmentSubmission,
    Course,
    CourseCategory,
    Lesson,
    LessonProgress,
)


def landing_page(request: HttpRequest):
    return render(request, "base/landing-page.html")


@login_required
def dashboard_view(request: HttpRequest):
    return render(request, "base/dashboard.html")


@login_required
def profile_view(request: HttpRequest):
    user = request.user

    context = {
        "user": user,
    }
    return render(request, "base/profile.html", context)


@login_required
def lesson_view(request: HttpRequest, course_title, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course__title=course_title)
    lesson_progress = LessonProgress.objects.get(
        lesson__id=lesson.id, student=request.user
    )
    course_lessons = Lesson.objects.filter(course=lesson.course)
    assignment_submission = AssignmentSubmission.objects.filter(
        assignment=lesson.assignment, student=request.user
    )
    if assignment_submission.exists():
        assignment_submission = assignment_submission.first()

    context = {
        "lesson": lesson,
        "course_lessons": course_lessons,
        "lesson_progress": lesson_progress,
        "assignment_submission": assignment_submission,
    }
    return render(request, "base/lesson.html", context)


@login_required
def courses_view(request: HttpRequest):
    courses = Course.objects.filter(status="Active")
    q = request.GET.get("q")
    category = request.GET.get("category")
    rating = request.GET.get("rating")
    difficulty = request.GET.get("difficulty")

    if q:
        courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Filter by category (optional)
    if category and category != "all":
        courses = courses.filter(category__name__iexact=category)

    # Filter by rating
    if rating and rating != "all":
        min_rating = int(rating[0])  # Converts "4+" to 4
        courses = [course for course in courses if course.rating >= min_rating]

    # Filter by difficulty
    if difficulty and difficulty != "all":
        courses = courses.filter(level=difficulty)

    context = {
        "courses": courses,
        "categories": CourseCategory.objects.all(),
    }
    return render(request, "base/courses.html", context)
