from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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
