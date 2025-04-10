from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        INSTRUCTOR = "instructor", _("Instructor")
        STUDENT = "student", _("Student")
        PARENT = "parent", _("Parent")

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_parent(self):
        return self.role == self.Role.PARENT

    def __str__(self):
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/%y/%m/%d",
        default="images/default-avatar.jpg",
        null=True,
        blank=True,
    )

    @property
    def avatar_url(self):
        if self.avatar:  # If an avatar is uploaded
            return self.avatar.url
        return "/images/default-avatar.jpg"


class StudentParentLink(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parent_links',
        limit_choices_to={'role': 'student'}
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_links',
        limit_choices_to={'role': 'parent'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'parent')

    def __str__(self):
        return f"{self.parent.username} -> {self.student.username}"
