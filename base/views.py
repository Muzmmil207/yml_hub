from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render

from courses.models import Course, CourseCategory


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
