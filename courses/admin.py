from django import forms
from django.contrib import admin

from .models import Assignment, Course, Enrollment, Lesson, Quiz


# Custom form to exclude instructor from visible fields
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "language"]

    def save(self, commit=True):
        course = super().save(commit=False)
        if not course.instructor_id:
            course.instructor = self.request.user
        if commit:
            course.save()
        return course


### Inlines for Quiz and Assignment inside LessonAdmin
class QuizInline(admin.TabularInline):  # Use StackedInline for more space
    model = Quiz
    extra = 1  # Number of empty forms displayed
    fields = ["title", "description", "max_score"]


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1
    fields = ["title", "instructions", "due_date", "max_score"]


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

    def save_model(self, request, obj, form, change):
        """Automatically assign instructor if not set."""
        if not obj.instructor_id:
            obj.instructor = request.user
        obj.save()


### Lesson Admin (With Quizzes and Assignments Inline)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order", "created_at"]
    exclude = ["instructor"]
    inlines = [QuizInline, AssignmentInline]  # Show Quiz & Assignment inside Lesson

    def get_queryset(self, request):
        """Admins see all lessons, instructors see only their own."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor=request.user)

    def save_model(self, request, obj, form, change):
        """Automatically assign instructor if not set."""
        if not obj.instructor_id:
            obj.instructor = request.user
        obj.save()


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled_at", "progress", "completed"]
    readonly_fields = ["student", "course", "enrolled_at", "progress", "completed"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "max_score"]


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "due_date", "max_score"]


# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Assignment, AssignmentAdmin)
