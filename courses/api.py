from rest_framework.decorators import api_view
from rest_framework.response import Response

from courses.models import Course, Lesson
from users.models import CustomUser


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
                "image": instructor.userprofile.avatar_url
            },
            "image": course.thumbnail_url,
            "duration": course.get_duration_display() if course.duration else "N/A",
            "level": course.get_level_display(),
            "students": f"{course.enrollment_set.count()}",
            "language": course.language,
            "rating": f"{course.rating} ({course.review_count})" if hasattr(course, 'rating') else "No ratings",
            "learningPoints": learning_points,
            "lessons": [
                {"title": lesson.title, "duration": lesson.get_duration_display(), "locked": True}
                for lesson in lessons
            ]
        }

        data.append(course_data)

    return Response(data)
