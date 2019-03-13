from django.db import models
from django.contrib.auth.models import User
from compositefk.fields import CompositeForeignKey


class Student(User):
    """ Students records in CanvasPath. """

    #email = models.CharField(max_length=50, primary_key=True)
    #password = models.CharField(max_length=50)
    name = models.CharField(max_length=25)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    major = models.CharField(max_length=25)
    street = models.CharField(max_length=25)
    zipcode = models.ForeignKey("courses.Zipcode", on_delete=models.DO_NOTHING)


class Zipcode(models.Model):
    """ Zipcodes for student addresses. """

    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)


class Professor(User):
    """ Professor records in CanvasPath. """

    #email = models.CharField(max_length=50, primary_key=True)
    #password = models.CharField(max_length=50)
    name = models.CharField(max_length=25)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    office_address = models.CharField(max_length=50)
    deptment = models.ForeignKey("courses.Department", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=25)


class Department(models.Model):
    """ Departments that students are enrolled in and professors
    teach in. """

    dept_name = models.CharField(max_length=25)
    dept_head = models.ForeignKey("courses.Professor", on_delete=models.DO_NOTHING)


class Course(models.Model):
    """ Courses that students take and professors teach. """

    course_name = models.CharField(max_length=25)
    course_description = models.CharField(max_length=250)


class Sections(models.Model):
    """ Sections for specific courses. """

    course_id = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    section_type = models.CharField(max_length=8)
    limit = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (("course_id", "sec_no"),)


class Enrolls(models.Model):
    """ Course enrollment for students. """

    student_email = models.ForeignKey("courses.Student", on_delete=models.CASCADE,
                                      to_field="email", db_column="email")
    course_id = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")

    class Meta:
        unique_together = (("student_email", "course_id", "sec_no"),)


class Prof_teams(models.Model):
    """ Teams of professors for teaching courses. """

    pass


class Prof_team_members(models.Model):
    """ Professors and their corresponding teams. """

    prof_email = models.ForeignKey("courses.Professor", on_delete=models.CASCADE,
                                   to_field="email", db_column="email")
    team_id = models.ForeignKey("courses.Prof_teams", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (("prof_email", "team_id"),)


class Homework(models.Model):
    """ Homework assigneents to be assigned to students from professors. """

    course_id = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    hw_no = models.PositiveSmallIntegerField()
    hw_details = models.CharField(max_length=250)

    class Meta:
        unique_together = (("course_id", "sec_no", "hw_no"),)


class Homework_grades(models.Model):
    """ Finalized grades for student homework assignments. """

    student_email = models.ForeignKey("courses.Student", on_delete=models.CASCADE,
                                      to_field="email", db_column="email")
    course_id = models.ForeignKey("courses.Homework", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Homework", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    hw_no = models.ForeignKey("courses.Homework", on_delete=models.CASCADE,
                              to_field="hw_no", db_column="hw_no")
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("student_email", "course_id", "sec_no", "hw_no"),)


class Exams(models.Model):
    """ Exams to be assigned to students from professors. """

    course_id = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    exam_no = models.PositiveSmallIntegerField()
    exam_details = models.CharField(max_length=250)

    class Meta:
        unique_together = (("course_id", "sec_no", "exam_no"),)


class Exam_grades(models.Model):
    """ Finalized grades for student exams. """

    student_email = models.ForeignKey("courses.Student", on_delete=models.CASCADE,
                                      to_field="email", db_column="email")
    course_id = models.ForeignKey("courses.Exams", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Exams", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    exam_no = models.ForeignKey("courses.Exams", on_delete=models.CASCADE,
                                to_field="exam_no", db_column="exam_no")
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("student_email", "course_id", "sec_no", "exam_no"),)


class Capstone_section(models.Model):
    """ Special course sections for senior capstone projects. """

    course_id = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Sections", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    project_no = models.PositiveSmallIntegerField()
    sponsor_id = models.ForeignKey("courses.Professor", on_delete=models.DO_NOTHING,
                                   to_field="email", db_column="email")

    class Meta:
        unique_together = (("course_id", "sec_no", "project_no"),)


class Capstone_team(models.Model):
    """ Capstone project teams. """

    course_id = models.ForeignKey("courses.Capstone_section", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Capstone_section", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    team_id = models.PositiveSmallIntegerField()
    project_no = models.ForeignKey("courses.Capstone_section", on_delete=models.DO_NOTHING,
                                   to_field="project_no", db_column="project_no")

    class Meta:
        unique_together = (("course_id", "sec_no", "team_id"),)


class Capstone_team_members(models.Model):
    """ Individual team members for capstone project teams. """

    student_email = models.ForeignKey("courses.Student", on_delete=models.CASCADE,
                                      to_field="email", db_column="email")
    team_id = models.ForeignKey("courses.Capstone_team", on_delete=models.DO_NOTHING,
                                to_field="team_id", db_column="team_id")
    course_id = models.ForeignKey("courses.Capstone_team", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Capstone_team", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")

    class Meta:
        unique_together = (("student_email", "team_id", "course_id", "sec_no"),)


class Capstone_grades(models.Model):
    """ Finalized grades for student capstone projects. """

    team_id = models.ForeignKey("courses.Capstone_team", on_delete=models.DO_NOTHING,
                                to_field="team_id", db_column="team_id")
    course_id = models.ForeignKey("courses.Capstone_team", on_delete=models.CASCADE,
                                  to_field="course_id", db_column="course_id")
    sec_no = models.ForeignKey("courses.Capstone_team", on_delete=models.CASCADE,
                               to_field="sec_no", db_column="sec_no")
    grade = models.CharField(max_length=1)

    class Meta:
        unique_together = (("team_id", "course_id", "sec_no"),)
