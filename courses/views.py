from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Student, Professor, Zipcode, Enrolls, Section, ProfTeamMember, Homework, HomeworkGrade, Exam, \
    ExamGrade
from .forms import HomeworkGradeFormset, ExamGradeFormset
import numpy as np


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

        homeworks = Homework.objects.filter(section=section, course=course)
        exams = Exam.objects.filter(section=section, course=course)

        homework_grades = []
        exam_grades = []
        students = []

        all_hw_avgs = []
        all_hw_mins = []
        all_hw_maxs = []

        all_exam_avgs = []
        all_exam_mins = []
        all_exam_maxs = []

        for homework in homeworks:
            initial_grades = HomeworkGrade.objects.filter(homework=homework, course=course, section=section).values_list("grade", flat=True)
            grades_list = list(filter(None, initial_grades))

            if len(grades_list) == 0:
                all_hw_avgs.append("N/A")
                all_hw_mins.append("N/A")
                all_hw_maxs.append("N/A")
            else:
                all_hw_avgs.append(sum(grades_list) / len(initial_grades))
                all_hw_mins.append(np.min(grades_list))
                all_hw_maxs.append(np.max(grades_list))

        for exam in exams:
            initial_grades = ExamGrade.objects.filter(exam=exam, course=course, section=section).values_list("grade", flat=True)
            grades_list = list(filter(None, initial_grades))

            if len(grades_list) == 0:
                all_exam_avgs.append("N/A")
                all_exam_mins.append("N/A")
                all_exam_maxs.append("N/A")
            else:
                all_exam_avgs.append(sum(grades_list) / len(initial_grades))
                all_exam_mins.append(np.min(grades_list))
                all_exam_maxs.append(np.max(grades_list))

        if is_student:

            # get course homework info
            for homework in homeworks:
                homework_grades.append(HomeworkGrade.objects.get(student=profile, course=course, section=section,
                                                                 homework=homework))

            # get course exam info
            for exam in exams:
                exam_grades.append(ExamGrade.objects.get(student=profile, course=course, section=section,
                                                         exam=exam))

        else:

            # get enrolled students
            enrolled = Enrolls.objects.filter(section=section, course=course)
            students = [enroll.student for enroll in enrolled]

        homeworks = zip(homeworks, all_hw_avgs, all_hw_mins, all_hw_maxs)
        exams = zip(exams, all_exam_avgs, all_exam_mins, all_exam_maxs)

        return render(request, "course_detail.html", {"section": section, "course": course, "professors": professors,
                                                      "exam_grades": exam_grades, "hw_grades": homework_grades,
                                                      "is_student": is_student, "students": students, "hws": homeworks,
                                                      "exams": exams})


class HomeworkDetail(View):
    """ Homework detail view to show grades for a professor's course. """

    def get(self, request, pk):

        homework = Homework.objects.get(id=pk)
        hw_grades = HomeworkGrade.objects.filter(homework=homework)
        hw_grade_formset = HomeworkGradeFormset(instance=homework)
        hw_grades = zip(hw_grades, hw_grade_formset)

        return render(request, "hw_detail.html", {"homework": homework, "hw_grades": hw_grades, "hw_grade_formset":
                                                  hw_grade_formset})

    def post(self, request, pk):

        homework = Homework.objects.get(id=pk)
        hw_grade_formset = HomeworkGradeFormset(request.POST, request.FILES, instance=homework)

        if hw_grade_formset.is_valid():
            hw_grade_formset.save()
        return redirect(homework.get_absolute_url())


class ExamDetail(View):
    """ Exam detail view to show grades for a professor's course. """

    def get(self, request, pk):

        exam = Exam.objects.get(id=pk)
        exam_grades = ExamGrade.objects.filter(exam=exam)
        exam_grade_formset = ExamGradeFormset(instance=exam)
        exam_grades = zip(exam_grades, exam_grade_formset)

        return render(request, "exam_detail.html", {"exam": exam, "exam_grades": exam_grades, "exam_grade_formset":
                                                    exam_grade_formset})

    def post(self, request, pk):
        exam = Exam.objects.get(id=pk)
        exam_grade_formset = ExamGradeFormset(request.POST, request.FILES, instance=exam)

        if exam_grade_formset.is_valid():
            exam_grade_formset.save()
        return redirect(exam.get_absolute_url())
