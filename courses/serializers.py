from rest_framework import serializers

from .models import AssignmentSubmission


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ["assignment", "attachment"]
