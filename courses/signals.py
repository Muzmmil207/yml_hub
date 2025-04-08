from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import AssignmentSubmission


@receiver(pre_save, sender=AssignmentSubmission)
def notify_student_on_review(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if new submission, not a review

    try:
        old_instance = AssignmentSubmission.objects.get(pk=instance.pk)
    except AssignmentSubmission.DoesNotExist:
        return

    # Send email only if score was just added
    if old_instance.score is None and instance.score is not None:
        student_email = instance.student.email
        subject = "Your Assignment Has Been Reviewed"
        message = (
            f"Hi {instance.student.first_name},\n\n"
            f"Your submission for '{instance.assignment.title}' has been reviewed.\n"
            f"Score: {instance.score}\n"
            f"Feedback: {instance.feedback or 'No feedback provided.'}\n\n"
            f"Thank you!"
        )

        send_mail(
            subject,
            message,
            "no-reply@yourdomain.com",  # Replace with your sender
            [student_email],
            fail_silently=False,
        )
