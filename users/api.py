from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserUpdateSerializer


class UpdateUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in via session

    def post(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        user_profile = request.user.userprofile
        user_profile.avatar = request.FILES["avatar"]
        user_profile.save()

        return JsonResponse({}, status=200)

    return JsonResponse({}, status=400)
