from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Student, Professor, Zipcode, Enrolls


class Home(View):
    """Homepage view."""

    def get(self, request):
        return render(request, "home.html")


class Profile(View):
    """ Profile view for users to see their basic information and change their password if needed. """

    def get(self, request):

        if request.user.is_student:
            profile = Student.objects.get(user=request.user)
            is_student = True
        else:
            profile = Professor.objects.get(user=request.user)
            is_student = False

        form = PasswordChangeForm(request.user)

        return render(request, "profile.html", {"form": form, "profile": profile, "is_student": is_student})

    def post(self, request):

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the error.")


class Dashboard(View):
    """ Courses dashboard for students to see courses they are enrolled in, and for professors to see courses they
    teach. """

    def get(self, request):

        if request.user.is_student:

            profile = Student.objects.get(user=request.user)

            enrolled = Enrolls.objects.filter(student=profile)


    def post(self, request):

        pass