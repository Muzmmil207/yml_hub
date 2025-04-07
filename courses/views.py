def enroll_in_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)

    if not created:
        # Already enrolled, get the last accessed lesson
        progress = (
            LessonProgress.objects.filter(user=user, lesson__course=course)
            .order_by("-updated_at")
            .first()
        )
        if progress:
            return redirect(f"/lessons/{progress.lesson.id}/")

    # New enrollment or no previous progress, redirect to first lesson
    first_lesson = Lesson.objects.filter(course=course).order_by("order").first()
    if first_lesson:
        return redirect(f"/lessons/{first_lesson.id}/")
    else:
        return Response({"detail": "No lessons found in this course."}, status=404)
