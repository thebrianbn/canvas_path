from django.db import models
from django.contrib.auth.models import User

User.add_to_class("is_student", models.BooleanField(default=False))


class Student(models.Model):
    """ Students records in CanvasPath. """

    name = models.CharField(max_length=25)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    major = models.CharField(max_length=25)
    street = models.CharField(max_length=25)
    zipcode = models.ForeignKey("courses.Zipcode", on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Zipcode(models.Model):
    """ Zipcodes for student addresses. """

    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)


class Professor(models.Model):
    """ Professor records in CanvasPath. """

    name = models.CharField(max_length=25)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    office_address = models.CharField(max_length=50)
    department = models.ForeignKey("courses.Department", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Department(models.Model):
    """ Departments that students are enrolled in and professors
    teach in. """

    dept_id = models.CharField(max_length=5)
    dept_name = models.CharField(max_length=25)
    dept_head = models.ForeignKey("courses.Professor", on_delete=models.DO_NOTHING, related_name="+", null=True)


class Course(models.Model):
    """ Courses that students take and professors teach. """

    course_name = models.CharField(max_length=25)
    course_description = models.CharField(max_length=250)


class Section(models.Model):
    """ Sections for specific courses. """

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.PositiveSmallIntegerField()
    section_type = models.CharField(max_length=8)
    limit = models.PositiveSmallIntegerField()
    prof_team = models.ForeignKey("courses.ProfTeams", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = (("course", "section"),)


class Enrolls(models.Model):
    """ Course enrollment for students. """

    student = models.ForeignKey("courses.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("student", "course", "section"),)


class ProfTeams(models.Model):
    """ Teams of professors for teaching courses. """

    team_id = models.PositiveSmallIntegerField()


class ProfTeamMember(models.Model):
    """ Professors and their corresponding teams. """

    professor = models.ForeignKey("courses.Professor", on_delete=models.CASCADE)
    team = models.ForeignKey("courses.ProfTeams", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (("professor", "team"),)


class Homework(models.Model):
    """ Homework assigneents to be assigned to students from professors. """

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE,)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE,)
    hw_no = models.PositiveSmallIntegerField()
    hw_details = models.CharField(max_length=250)

    class Meta:
        unique_together = (("course", "section", "hw_no"),)


class HomeworkGrade(models.Model):
    """ Finalized grades for student homework assignments. """

    student = models.ForeignKey("courses.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    homework = models.ForeignKey("courses.Homework", on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("student", "course", "section", "homework"),)


class Exam(models.Model):
    """ Exams to be assigned to students from professors. """

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    exam_no = models.PositiveSmallIntegerField()
    exam_details = models.CharField(max_length=250)

    class Meta:
        unique_together = (("course", "section", "exam_no"),)


class ExamGrade(models.Model):
    """ Finalized grades for student exams. """

    student = models.ForeignKey("courses.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    exam = models.ForeignKey("courses.Exam", on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("student", "course", "section", "exam"),)


class CapstoneSection(models.Model):
    """ Special course sections for senior capstone projects. """

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    project_no = models.PositiveSmallIntegerField()
    sponsor = models.ForeignKey("courses.Professor", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (("course", "section", "project_no"),)


class CapstoneTeam(models.Model):
    """ Capstone project teams. """

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    team_id = models.PositiveSmallIntegerField()
    project = models.ForeignKey("courses.CapstoneSection", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (("course", "section", "team_id"),)


class CapstoneTeamMember(models.Model):
    """ Individual team members for capstone project teams. """

    student = models.ForeignKey("courses.Student", on_delete=models.CASCADE)
    team = models.ForeignKey("courses.CapstoneTeam", on_delete=models.DO_NOTHING)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("student", "team", "course", "section"),)


class Capstone_grades(models.Model):
    """ Finalized grades for student capstone projects. """

    team = models.ForeignKey("courses.CapstoneTeam", on_delete=models.DO_NOTHING)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("team", "course", "section"),)
