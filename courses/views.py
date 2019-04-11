from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Student, Professor, Zipcode, Enrolls, Section, ProfTeamMember, Homework, HomeworkGrade, Exam, \
    ExamGrade
from .forms import HomeworkGradeFormset, ExamGradeFormset, HomeworkCreationForm, ExamCreationForm
import numpy as np


class Home(View):
    """Homepage view."""

    def get(self, request):

        return render(request, "home.html")


class Profile(View):
    """ Profile view for users to see their basic information and change their password if needed. """

    def get(self, request):

        # get user profile
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

        # update password if password is valid
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Invalid password.")


class Dashboard(View):
    """ Courses dashboard for students to see courses they are enrolled in, and for professors to see courses they
    teach. """

    def get(self, request):

        # get user profile and course sections
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

        # get user profile
        if request.user.is_student:
            profile = Student.objects.get(user=request.user)
            is_student = True
        else:
            profile = Professor.objects.get(user=request.user)
            is_student = False

        # query for all relevant instances
        section = Section.objects.get(id=pk)
        course = section.course
        prof_team = section.prof_team
        team_members = ProfTeamMember.objects.filter(team=prof_team)
        professors = [team_member.professor for team_member in team_members]
        homeworks = Homework.objects.filter(section=section, course=course)
        exams = Exam.objects.filter(section=section, course=course)

        # keep track of a student's grades
        homework_grades = []
        exam_grades = []
        students = []

        # keep track of all homework statistics
        all_hw_avgs = []
        all_hw_mins = []
        all_hw_maxs = []

        # keep track of all exam statistics
        all_exam_avgs = []
        all_exam_mins = []
        all_exam_maxs = []

        # for each homework, make avg, min, and max calculations
        for homework in homeworks:
            initial_grades = HomeworkGrade.objects.filter(homework=homework, course=course, section=section).values_list("grade", flat=True)
            grades_list = list(filter(None, initial_grades))

            # if there are no grades, no available statistics
            if len(grades_list) == 0:
                all_hw_avgs.append("N/A")
                all_hw_mins.append("N/A")
                all_hw_maxs.append("N/A")
            else:
                all_hw_avgs.append("%0.2f" % (sum(grades_list) / len(grades_list)))
                all_hw_mins.append(np.min(grades_list))
                all_hw_maxs.append(np.max(grades_list))

        # for each exam, make avg, min, and max calculations
        for exam in exams:
            initial_grades = ExamGrade.objects.filter(exam=exam, course=course, section=section).values_list("grade",
                                                                                                             flat=True)
            grades_list = list(filter(None, initial_grades))

            # if there are no grades, no available statistics
            if len(grades_list) == 0:
                all_exam_avgs.append("N/A")
                all_exam_mins.append("N/A")
                all_exam_maxs.append("N/A")
            else:
                all_exam_avgs.append("%0.2f" % (sum(grades_list) / len(grades_list)))
                all_exam_mins.append(np.min(grades_list))
                all_exam_maxs.append(np.max(grades_list))

        # if the user is a student, query for their grades, if professor, get a list of their students for the course
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

        # zip statistics with assignments
        homeworks = zip(homeworks, all_hw_avgs, all_hw_mins, all_hw_maxs)
        exams = zip(exams, all_exam_avgs, all_exam_mins, all_exam_maxs)
        homework_grades = zip(homework_grades, all_hw_avgs, all_hw_mins, all_hw_maxs)
        exam_grades = zip(exam_grades, all_exam_avgs, all_exam_mins, all_exam_maxs)

        return render(request, "course_detail.html", {"section": section, "course": course, "professors": professors,
                                                      "exam_grades": exam_grades, "hw_grades": homework_grades,
                                                      "is_student": is_student, "students": students, "hws": homeworks,
                                                      "exams": exams})


class HomeworkDetail(View):
    """ Homework detail view to show grades for a professor's course. """

    def get(self, request, pk):

        # query the homework instance and create formset
        homework = Homework.objects.get(id=pk)
        hw_grades = HomeworkGrade.objects.filter(homework=homework)
        hw_grade_formset = HomeworkGradeFormset(instance=homework)
        hw_grades = zip(hw_grades, hw_grade_formset)

        return render(request, "hw_detail.html", {"homework": homework, "hw_grades": hw_grades, "hw_grade_formset":
                                                  hw_grade_formset})

    def post(self, request, pk):

        # query the homework instance and get formset from POST request
        homework = Homework.objects.get(id=pk)
        hw_grade_formset = HomeworkGradeFormset(request.POST, request.FILES, instance=homework)
        section = homework.section

        # if all grades were submitted, save results
        if hw_grade_formset.is_valid():
            hw_grade_formset.save()
        else:
            messages.error(request, "All grades must be submitted at once")

        return redirect(section.get_absolute_url())


class ExamDetail(View):
    """ Exam detail view to show grades for a professor's course. """

    def get(self, request, pk):

        # query the exam instance and create formset
        exam = Exam.objects.get(id=pk)
        exam_grades = ExamGrade.objects.filter(exam=exam)
        exam_grade_formset = ExamGradeFormset(instance=exam)
        exam_grades = zip(exam_grades, exam_grade_formset)

        return render(request, "exam_detail.html", {"exam": exam, "exam_grades": exam_grades, "exam_grade_formset":
                                                    exam_grade_formset})

    def post(self, request, pk):

        # query the exam instance and retrieve formset from POST request
        exam = Exam.objects.get(id=pk)
        exam_grade_formset = ExamGradeFormset(request.POST, request.FILES, instance=exam)
        section = exam.section

        # if all grades were submitted, save results
        if exam_grade_formset.is_valid():
            exam_grade_formset.save()
        else:
            messages.error(request, "All grades must be submitted at once.")

        return redirect(section.get_absolute_url())


class HomeworkCreation(View):
    """ View for professors to create homeworks for a specific course section. """

    def get(self, request, pk):

        # query the section instance and create form
        section = Section.objects.get(id=pk)
        form = HomeworkCreationForm(instance=section)

        return render(request, "assignment_creation.html", {"form": form, "assignment_type": "Homework"})

    def post(self, request, pk):

        # query relevant instances and get formset from POST request
        section = Section.objects.get(id=pk)
        course = section.course
        enrolled = Enrolls.objects.filter(section=section, course=course)
        students = [enroll.student for enroll in enrolled]
        form = HomeworkCreationForm(request.POST)

        # if homework information entered correctly, save results
        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.section = section
            new_instance.course = section.course
            new_instance.save()

            # for each student in the course section, create new homework grade instances
            for student in students:
                new_hw_grade = HomeworkGrade(section=section, course=course, student=student, homework=new_instance,
                                             grade=None)
                new_hw_grade.save()
        else:
            messages.error(request, "Error in homework creation.")

        return redirect(section.get_absolute_url())


class ExamCreation(View):
    """ View for professors to create homeworks for a specific course section. """

    def get(self, request, pk):

        # query the section instance and create form
        section = Section.objects.get(id=pk)
        form = ExamCreationForm(instance=section)

        return render(request, "assignment_creation.html", {"form": form, "assignment_type": "Exam"})

    def post(self, request, pk):

        # query relevant instances and get formset from POST request
        section = Section.objects.get(id=pk)
        course = section.course
        enrolled = Enrolls.objects.filter(section=section, course=course)
        students = [enroll.student for enroll in enrolled]
        form = ExamCreationForm(request.POST)

        # if exam information entered correctly, save results
        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.section = section
            new_instance.course = section.course
            new_instance.save()

            # for each student in the course section, create new exam grade instances
            for student in students:
                new_exam_grade = ExamGrade(section=section, course=course, student=student, exam=new_instance,
                                           grade=None)
                new_exam_grade.save()
        else:
            messages.error(request, "Error in exam creation.")

        return redirect(section.get_absolute_url())
