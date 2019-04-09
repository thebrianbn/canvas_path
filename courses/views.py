from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Student, Professor, Zipcode, Enrolls, Section, ProfTeamMember, Homework, HomeworkGrade, Exam, \
    ExamGrade


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

            is_student = True
            profile = Student.objects.get(user=request.user)
            enrolled = Enrolls.objects.filter(student=profile)
            sections = [enroll.section for enroll in enrolled]

        else:

            is_student = False
            profile = Professor.objects.get(user=request.user)
            prof_team = ProfTeamMember.objects.get(professor=profile).team
            sections = Section.objects.filter(prof_team=prof_team)

        return render(request, "dashboard.html", {"sections": sections, "is_student": is_student})


class CourseDetail(View):
    """ Course detail view to show course and professor information."""

    def get(self, request, pk):

        if request.user.is_student:
            profile = Student.objects.get(user=request.user)
            is_student = True
        else:
            profile = Professor.objects.get(user=request.user)
            is_student = False

        section = Section.objects.get(id=pk)
        course = section.course
        prof_team = section.prof_team
        team_members = ProfTeamMember.objects.filter(team=prof_team)
        professors = [team_member.professor for team_member in team_members]

        homework_grades = []
        exam_grades = []

        if is_student:

            # get course homework info
            homeworks = Homework.objects.filter(section=section, course=course)
            for homework in homeworks:
                homework_grades.append(HomeworkGrade.objects.get(student=profile, course=course, section=section,
                                                                 homework=homework))

            # get course exam info
            exams = Exam.objects.filter(section=section, course=course)
            for exam in exams:
                exam_grades.append(ExamGrade.objects.get(student=profile, course=course, section=section,
                                                         exam=exam))

        return render(request, "course_detail.html", {"section": section, "course": course, "professors": professors,
                                                      "exam_grades": exam_grades, "hw_grades": homework_grades,
                                                      "is_student": is_student})
