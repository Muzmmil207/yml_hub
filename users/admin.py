from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, StudentParentLink


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(StudentParentLink)
class StudentParentLinkAdmin(admin.ModelAdmin):
    list_display = ("parent_username", "student_username", "created_at")
    list_filter = ("created_at",)
    search_fields = ("parent__username", "student__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def parent_username(self, obj):
        return obj.parent.username

    parent_username.short_description = "Parent Username"

    def student_username(self, obj):
        return obj.student.username

    student_username.short_description = "Student Username"

    class Meta:
        verbose_name = "Student-Parent Link"
        verbose_name_plural = "Student-Parent Links"
