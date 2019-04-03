from django.urls import path
from courses.views import Home, PasswordChange

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/", PasswordChange.as_view(), name="profile")
]