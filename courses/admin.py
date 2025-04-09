from django import forms
from django.contrib import admin

from quizzes.models import Quiz

from .models import (
    Assignment,
    AssignmentSubmission,
    Course,
    CourseCategory,
    CourseReview,
    Enrollment,
    Lesson,
)


# Custom form to exclude instructor from visible fields
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "language",
            "instructor",
            "category",
            "status",
            "thumbnail",
            "duration",
            "level",
            "learning_points",
        ]

    def save(self, commit=True):
        course = super().save(commit=False)
        if not hasattr(course, "instructor"):
            course.instructor = self.request.user
        if commit:
            course.save()
        return course


### Inlines for Quiz and Assignment inside LessonAdmin
class QuizInline(admin.TabularInline):  # Use StackedInline for more space
    model = Quiz
    extra = 1  # Number of empty forms displayed
    fields = ["title", "description"]


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1
    fields = ["title", "instructions", "due_date"]


### Inline for Lesson inside CourseAdmin
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    exclude = ["instructor"]  # Hide instructor field


### Course Admin (With Lessons Inline)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ["title", "instructor", "language", "created_at"]
    exclude = ["instructor"]
    list_filter = ["language"]
    search_fields = ["title", "instructor__username"]
    inlines = [LessonInline]  # Show Lessons inside CourseAdmin

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request  # Pass request to form
        return form

    def get_queryset(self, request):
        """Admins see all courses, instructors see only their own."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor=request.user)


### Lesson Admin (With Quizzes and Assignments Inline)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "created_at"]
    exclude = ["instructor"]
    inlines = [QuizInline, AssignmentInline]  # Show Quiz & Assignment inside Lesson

    def get_queryset(self, request):
        """Admins see all lessons, instructors see only their own."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor=request.user)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled_at", "progress", "completed"]
    readonly_fields = ["student", "course", "enrolled_at", "progress", "completed"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "due_date", "max_score"]


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "user", "rating", "created_at")
    search_fields = ("course__name", "user__username")
    list_filter = ("rating", "created_at")


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "score")
    list_filter = ("assignment", "score", "is_reviewed")
    search_fields = ("student__username", "assignment__title")

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing submission
            return ("assignment", "student")
        return ()


# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)
