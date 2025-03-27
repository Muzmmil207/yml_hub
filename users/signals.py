from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def handle_user_creation(sender, instance: CustomUser, created, **kwargs):
    if created:
        # If role is instructor, make them staff
        if instance.role == CustomUser.Role.INSTRUCTOR:
            instance.is_staff = True
            instance.save()

        # Send Welcome Email
        login_url = f"{settings.SITE_URL}{reverse('login')}"
        subject = "Welcome to Our Platform!"
        message = f"""
        Hi {instance.username},

        Your account has been created successfully.
        You can login here: {login_url}

        Role: {instance.role.capitalize()}

        Thank you!
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
