from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("ar", "Arabic"),
]


class Course(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Enter the course title (max 255 characters).",
        verbose_name="Course Title",
    )
    description = models.TextField(help_text="Provide a detailed course description.")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["admin", "instructor"]},
        help_text="Select the instructor for this course. Only admins and instructors are allowed.",
        verbose_name="Instructor",
    )
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        default="en",
        help_text="Specify the course language. Default is Arabic.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the course was created."
    )
    status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Archived", "Archived")],
        default="Active",
        help_text="Set the course status.",
    )
    thumbnail = models.ImageField(
        upload_to="course_thumbnails/",
        blank=True,
        null=True,
        help_text="Upload a thumbnail image for the course.",
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        help_text="Select the student enrolling in this course.",
        verbose_name="Enrolled Student",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, help_text="Choose the course for enrollment."
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the student enrolled in the course.",
        verbose_name="Enrollment Date",
    )
    progress = models.FloatField(
        default=0.0,
        help_text="Track the student's progress as a percentage (0.0 - 100.0).",
        verbose_name="Course Progress",
    )
    completed = models.BooleanField(
        default=False,
        help_text="Indicates whether the student has completed the course.",
        verbose_name="Completed",
    )

    class Meta:
        unique_together = ("student", "course")
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Select the course this lesson belongs to.",
        verbose_name="Course",
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["admin", "instructor"]},
        help_text="Choose the instructor responsible for this lesson.",
        verbose_name="Instructor",
    )
    title = models.CharField(
        max_length=255,
        help_text="Enter the lesson title (max 255 characters).",
        verbose_name="Lesson Title",
    )
    content = RichTextField(
        help_text="Provide the lesson content. You can use formatted text if supported.",
        verbose_name="Lesson Content",
    )  # Consider using a RichTextField if available
    video_url = models.URLField(
        blank=True, null=True, help_text="Link to a lesson video (if available)."
    )
    attachments = models.FileField(
        upload_to="lesson_attachments/",
        blank=True,
        null=True,
        help_text="Upload additional lesson materials.",
    )
    order = models.PositiveIntegerField(
        help_text="Define the lesson order within the course.",
        verbose_name="Lesson Order",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the lesson was created.",
        verbose_name="Created At",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Course Lesson"
        verbose_name_plural = "Course Lessons"

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Assignment(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="assignments",
        help_text="Select the lesson this assignment belongs to.",
        verbose_name="Lesson",
    )
    title = models.CharField(
        max_length=255,
        help_text="Enter the assignment title (max 255 characters).",
        verbose_name="Assignment Title",
    )
    instructions = RichTextField(
        help_text="Provide detailed instructions for completing the assignment.",
        verbose_name="Assignment Instructions",
    )
    due_date = models.DateTimeField(
        help_text="Specify the due date and time for this assignment.",
        verbose_name="Due Date",
    )
    max_score = models.PositiveIntegerField(
        default=100,
        help_text="Set the maximum score a student can achieve in this assignment.",
        verbose_name="Maximum Score",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the assignment was created.",
        verbose_name="Created At",
    )

    def __str__(self):
        return f"Assignment: {self.title} (Lesson: {self.lesson.title})"

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
