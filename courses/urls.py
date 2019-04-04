from django.urls import path
from courses.views import Home, Profile, Dashboard, CourseDetail

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/", Profile.as_view(), name="profile"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path('jobs/<int:pk>/', CourseDetail.as_view(), name="course-detail"),
]