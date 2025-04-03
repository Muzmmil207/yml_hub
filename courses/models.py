from django.conf import settings
from django.db import models
from django.db.models import Avg, Count
from django_ckeditor_5.fields import CKEditor5Field

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("ar", "Arabic"),
]


class CourseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    DURATION_CHOICES = [
        ("1_day", "1 Day"),
        ("3_days", "3 Days"),
        ("1_week", "1 Week"),
        ("2_weeks", "2 Weeks"),
        ("4_weeks", "4 Weeks"),
        ("8_weeks", "8 Weeks"),
        ("12_weeks", "12 Weeks"),
    ]

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

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
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Select the category this course belongs to (e.g., JavaScript, React, Python, Flutter, Node, Unity).",
        verbose_name="Course Category",
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
    duration = models.CharField(
        max_length=10,
        choices=DURATION_CHOICES,
        help_text="Select the total duration of the course (e.g., 1 Day, 1 Week, 4 Weeks).",
        verbose_name="Course Duration",
    )
    level = models.CharField(
        max_length=15,
        choices=LEVEL_CHOICES,
        default="beginner",
        help_text="Select the difficulty level of the course.",
        verbose_name="Course Level",
    )
    learning_points = models.TextField(
        help_text="Enter key learning points separated by semicolons (;). Example: Learn Python basics; Understand OOP; Work with Django",
        verbose_name="Learning Points",
    )

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        if self.thumbnail:  # If an thumbnail is uploaded
            return self.thumbnail.url
        return "/images/default-thumbnail.jpg"

    @property
    def rating(self):
        """Returns the average rating of the course."""
        return self.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0

    @property
    def review_count(self):
        """Returns the total number of reviews for the course."""
        return self.reviews.aggregate(count=Count("id"))["count"]


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} Stars") for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} Stars"


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
    DURATION_CHOICES = [
        ("5_min", "5 Minutes"),
        ("10_min", "10 Minutes"),
        ("15_min", "15 Minutes"),
        ("30_min", "30 Minutes"),
        ("45_min", "45 Minutes"),
        ("1_hour", "1 Hour"),
        ("1.5_hours", "1.5 Hours"),
        ("2_hours", "2 Hours"),
    ]
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
    content = CKEditor5Field(
        help_text="Provide the lesson content. You can use formatted text if supported.",
        verbose_name="Lesson Content",
    )  # Consider using a CKEditor5Field if available
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
    duration = models.CharField(
        max_length=10,
        choices=DURATION_CHOICES,
        help_text="Select the estimated duration of the lesson (e.g., 10 Minutes, 30 Minutes, 1 Hour).",
        verbose_name="Lesson Duration",
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
    instructions = CKEditor5Field(
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
