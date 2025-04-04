from django.urls import path

from . import api
from .views import login_view, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # API
    path(
        "api/update-profile/",
        api.UpdateUserProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "api/update-profile-picture/",
        api.update_profile_picture,
        name="update_profile_picture",
    ),
]
