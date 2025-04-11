from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from courses.models import (
    AssignmentSubmission,
    Course,
    CourseCategory,
    CourseReview,
    Enrollment,
    Lesson,
    LessonProgress,
)
from quizzes.models import QuizAttempt
from users.models import StudentParentLink


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
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson_progress, _ = LessonProgress.objects.get_or_create(
        lesson=lesson, student=request.user
    )

    # Get next lesson (greater id in the same course)
    next_lesson = (
        Lesson.objects.filter(course=lesson.course, id__gt=lesson.id)
        .order_by("id")
        .first()
    )

    # Get previous lesson (smaller id in the same course)
    previous_lesson = (
        Lesson.objects.filter(course=lesson.course, id__lt=lesson.id)
        .order_by("-id")
        .first()
    )

    course_lessons = list()
    for course_lesson in Lesson.objects.filter(course=lesson.course):
        is_completed = False
        course_lesson_progress = LessonProgress.objects.filter(
            lesson__id=course_lesson.id, student=request.user
        )
        if course_lesson_progress.exists():
            is_completed = course_lesson_progress[0].completed

        course_lessons.append(
            {
                "id": course_lesson.id,
                "title": course_lesson.title,
                "is_completed": is_completed,
            }
        )

    try:
        assignment_submission = AssignmentSubmission.objects.filter(
            assignment=lesson.assignment, student=request.user
        )
        if assignment_submission.exists():
            assignment_submission = assignment_submission.first()
    except:
        assignment_submission = None
    quizzes = lesson.quizzes.all()

    # Get all quiz attempts by this user for this lesson
    attempts = QuizAttempt.objects.filter(
        student=request.user, quiz__in=quizzes
    ).select_related("quiz")

    # Map attempts by quiz id for easier lookup in template
    attempts_dict = {attempt.quiz.id: attempt for attempt in attempts}

    context = {
        "lesson": lesson,
        "course_lessons": course_lessons,
        "lesson_progress": lesson_progress,
        "assignment_submission": assignment_submission,
        "attempts": attempts_dict,
        "course_title": course_title,
        "next_lesson": next_lesson,
        "previous_lesson": previous_lesson,
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


@login_required
def course_view(request: HttpRequest, course_slug, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_reviews = CourseReview.objects.filter(course=course)
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

    context = {
        "course": course,
        "enrollment": enrollment,
        "course_reviews": course_reviews,
    }
    return render(request, "base/course.html", context)


DURATION_TO_HOURS = {
    "5_min": 5 / 60,
    "10_min": 10 / 60,
    "15_min": 15 / 60,
    "30_min": 30 / 60,
    "45_min": 45 / 60,
    "1_hour": 1,
    "1.5_hours": 1.5,
    "2_hours": 2,
}


def get_total_badges_earned(completed_lessons_count):
    badges = [
        1,
        5,
        10,
        25,
        50,
    ]

    earned = [threshold for threshold in badges if completed_lessons_count >= threshold]
    return len(earned)


@login_required
def student_dashboard(request: HttpRequest):
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    progress = LessonProgress.objects.filter(
        student=request.user, completed=True
    ).select_related("lesson")
    hours_spent = sum(DURATION_TO_HOURS.get(lp.lesson.duration, 0) for lp in progress)

    completed_lessons = progress.count()

    total_badges_earned = get_total_badges_earned(completed_lessons)
    context = {
        "enrolled_courses": enrolled_courses,
        "completed_lessons": completed_lessons,
        "hours_spent": round(hours_spent, 2),
        "total_badges_earned": total_badges_earned,
    }
    return render(request, "base/student-dashboard.html", context)


@login_required
def parent_dashboard(request):
    if request.user.role != "parent":
        return redirect("landing")

    context = {}
    return render(request, "base/parent-dashboard.html", context)
