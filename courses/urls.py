from django.urls import path
from courses.views import Home, Profile, Dashboard, CourseDetail, HomeworkDetail
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/", Profile.as_view(), name="profile"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path('courses/<int:pk>/', CourseDetail.as_view(), name="course-detail"),
    path('homeworks/<int:pk>/', HomeworkDetail.as_view(), name="hw-detail"),
    #path('exams/<int:pk>/', ExamDetail.as_view(), name="exam-detail"),
]