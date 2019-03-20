from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', TemplateView.as_view(template_name="index.html")),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
