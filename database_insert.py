import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "canvas_path.settings")
import django
django.setup()
from courses.models import *


def populate_users(user_data):

    for i in range(len(user_data)):

        new_user = User()
        new_user.username = user_data.loc[i, :]["Email"]
        new_user.email = user_data.loc[i, :]["Email"]
        new_user.password = user_data.loc[i, :]["Password"]
        new_user.save()


def popular_zipcodes(zipcode_data):

    for i in range(len(zipcode_data)):

        new_zipcode = Zipcode()
        new_zipcode.zipcode = zipcode_data.loc[i, :]["Zip"]
        new_zipcode.city = zipcode_data.loc[i, :]["City"]
        new_zipcode.state = zipcode_data.loc[i, :]["State"]
        new_zipcode.save()


def populate_students(student_data):

    for i in range(len(student_data)):

        # corresponding user instance
        user = User.objects.get(email=students.loc[i, :]["Email"])
        # corresponding zipcode instance
        zipcode = Zipcode.objects.get(zipcode=student_data.loc[i, :]["Zip"])

        new_student = Student()
        new_student.name = student_data.loc[i, :]["Full Name"]
        new_student.age = student_data.loc[i, :]["Age"]
        new_student.gender = student_data.loc[i, :]["Gender"]
        new_student.street = student_data.loc[i, :]["Street"]
        new_student.major = student_data.loc[i, :]["Major"]
        new_student.phone = student_data.loc[i, :]["Phone"]
        new_student.user = user
        new_student.zipcode = zipcode
        new_student.save()


def populate_courses(course_data):

    for i in range(len(course_data)):

        new_course = Course()
        new_course.course_name = course_data.loc[i, :]["Course"]
        new_course.course_description = course_data.loc[i, :]["Details"]
        new_course.save()


def populate_sections(section_data):

    for i in range(len(section_data)):

        # corresponding course instance
        course = Course.objects.get(course_name=section_data.loc[i, :]["Course"])

        if len(Section.objects.filter(course=course, section=section_data.loc[i, :]["Section"])) != 0:
            continue

        new_section = Section()
        new_section.course = course
        new_section.section = section_data.loc[i, :]["Section"]
        new_section.section_type = section_data.loc[i, :]["Type"]
        new_section.limit = section_data.loc[i, :]["Limit"]
        new_section.save()


def populate_departments(department_data):

    for i in range(len(department_data)):

        new_department = Department()
        new_department.dept_id = department_data.loc[i, :]["Department"]
        new_department.dept_name = department_data.loc[i, :]["Department Name"]
        new_department.save()


def populate_professors(professor_data):

    for i in range(len(professor_data)):

        # corresponding department
        department = Department.objects.get(dept_id=professor_data.loc[i, :]["Department"])
        # corresponding user instance
        user = User.objects.get(email=students.loc[i, :]["Email"])

        new_professor = Professor()
        new_professor.name = professor_data.loc[i, :]["Name"]
        new_professor.age = professor_data.loc[i, :]["Age"]
        new_professor.gender = professor_data.loc[i, :]["Gender"]
        new_professor.office_address = professor_data.loc[i, :]["Office"]
        new_professor.title = professor_data.loc[i, :]["Title"]
        new_professor.department = department
        new_professor.user = user
        new_professor.save()

        if professor_data.loc[i, :]["Title"] == "Head":
            department.dept_head = Professor.objects.get(name=professor_data.loc[i, :]["Name"])
            department.save()


def populate_enrolls(enrolls_data):

    for i in range(len(enrolls_data)):

        # corresponding student
        student = Student.objects.get(name=enrolls_data.loc[i, :]["Full Name"])
        # corresponding courses
        course1 = Course.objects.get(course_name=enrolls_data.loc[i, :]["Courses 1"])
        course2 = Course.objects.get(course_name=enrolls_data.loc[i, :]["Courses 2"])
        course3 = Course.objects.get(course_name=enrolls_data.loc[i, :]["Courses 3"])
        # corresponding sections
        section1 = Section.objects.get(course=course1, section=enrolls_data.loc[i, :]["Course 1 Section"])
        section2 = Section.objects.get(course=course2, section=enrolls_data.loc[i, :]["Course 2 Section"])
        section3 = Section.objects.get(course=course3, section=enrolls_data.loc[i, :]["Course 3 Section"])

        new_enrolls1 = Enrolls(student=student, course=course1, section=section1)
        new_enrolls2 = Enrolls(student=student, course=course2, section=section2)
        new_enrolls3 = Enrolls(student=student, course=course3, section=section3)

        new_enrolls1.save()
        new_enrolls2.save()
        new_enrolls3.save()


def populate_prof_teams(prof_team_data):

    for i in range(len(prof_team_data)):

        new_prof_team = ProfTeams(team_id=prof_team_data.loc[i, :]["Team ID"])
        new_prof_team.save()


def populate_prof_team_members(prof_team_member_data):

    for i in range(len(prof_team_data)):

        # corresponding professor instance
        professor = Professor.objects.get(name=prof_team_member_data.loc[i, :]["Name"])
        # corresponding team instance
        team = ProfTeams.objects.get(team_id=prof_team_member_data.loc[i, :]["Team ID"])

        new_prof_team_member = ProfTeamMember(professor=professor, team=team)
        new_prof_team_member.save()


def populate_homeworks(homework_data):

    for i in range(len(homework_data)):

        # corresponding course instance
        course = Course.objects.get(course_name=homework_data.loc[i, :]["Course"])
        # corresponding section instance
        section = Section.objects.get(course=course, section=homework_data.loc[i, :]["Section"])

        new_homework = Homework()
        new_homework.course = course
        new_homework.section = section
        new_homework.hw_no = homework_data.loc[i, :]["HW_No"]
        new_homework.hw_details = homework_data.loc[i, :]["HW_Details"]
        new_homework.save()


def populate_homework_grades(homework_grade_data):

    for i in range(len(homework_grade_data)):

        # corresponding student
        student = Student.objects.get(name=homework_grade_data.loc[i, :]["Full Name"])
        # corresponding courses
        course1 = Course.objects.get(course_name=homework_grade_data.loc[i, :]["Courses 1"])
        course2 = Course.objects.get(course_name=homework_grade_data.loc[i, :]["Courses 2"])
        course3 = Course.objects.get(course_name=homework_grade_data.loc[i, :]["Courses 3"])
        # corresponding sections
        section1 = Section.objects.get(course=course1, section=homework_grade_data.loc[i, :]["Course 1 Section"])
        section2 = Section.objects.get(course=course2, section=homework_grade_data.loc[i, :]["Course 2 Section"])
        section3 = Section.objects.get(course=course3, section=homework_grade_data.loc[i, :]["Course 3 Section"])
        # corresponding homeworks
        homework1 = Homework.objects.get(course=course1, section=section1,
                                         hw_no=homework_grade_data.loc[i, :]["Course 1 HW_No"])
        homework2 = Homework.objects.get(course=course2, section=section2,
                                         hw_no=homework_grade_data.loc[i, :]["Course 2 HW_No"])
        homework3 = Homework.objects.get(course=course3, section=section3,
                                         hw_no=homework_grade_data.loc[i, :]["Course 3 HW_No"])

        new_homework_grade1 = HomeworkGrade()
        new_homework_grade1.student = student
        new_homework_grade1.course = course1
        new_homework_grade1.section = section1
        new_homework_grade1.homework = homework1
        new_homework_grade1.grade = homework_grade_data.loc[i, :]["Course 1 HW_Grade"]

        new_homework_grade2 = HomeworkGrade()
        new_homework_grade2.student = student
        new_homework_grade2.course = course2
        new_homework_grade2.section = section2
        new_homework_grade2.homework = homework2
        new_homework_grade2.grade = homework_grade_data.loc[i, :]["Course 2 HW_Grade"]

        new_homework_grade3 = HomeworkGrade()
        new_homework_grade3.student = student
        new_homework_grade3.course = course3
        new_homework_grade3.section = section3
        new_homework_grade3.homework = homework3
        new_homework_grade3.grade = homework_grade_data.loc[i, :]["Course 3 HW_Grade"]

        new_homework_grade1.save()
        new_homework_grade2.save()
        new_homework_grade3.save()


if __name__ == "__main__":

    students = pd.read_csv("Students.csv")
    professors = pd.read_csv("Professors.csv")

    user_data_students = students.loc[:, ["Email", "Password"]]
    user_data_professors = professors.loc[:, ["Email", "Password"]]
    user_data = pd.concat([user_data_students, user_data_professors], axis=0).drop_duplicates().reset_index()

    zipcode_data = students.loc[:, ["Zip", "City", "State"]].drop_duplicates().reset_index()
    student_data = students.loc[:, ["Full Name", "Age", "Gender", "Street", "Major", "Phone", "Email", "Zip"]]

    course1_data = students.loc[:, ["Courses 1", "Course 1 Details"]]
    course1_data.columns = ["Course", "Details"]
    course2_data = students.loc[:, ["Courses 2", "Course 2 Details"]]
    course2_data.columns = ["Course", "Details"]
    course3_data = students.loc[:, ["Courses 3", "Course 3 Details"]]
    course3_data.columns = ["Course", "Details"]
    course_data = pd.concat([course1_data, course2_data, course3_data], axis=0).drop_duplicates().reset_index()

    section1_data = students.loc[:, ["Courses 1", "Course 1 Section", "Course 1 Type", "Course 1 Section Limit"]]
    section1_data.columns=["Course", "Section", "Type", "Limit"]
    section2_data = students.loc[:, ["Courses 2", "Course 2 Section", "Course 2 Type", "Course 2 Section Limit"]]
    section2_data.columns = ["Course", "Section", "Type", "Limit"]
    section3_data = students.loc[:, ["Courses 3", "Course 3 Section", "Course 3 Type", "Course 3 Section Limit"]]
    section3_data.columns = ["Course", "Section", "Type", "Limit"]
    section_data = pd.concat([section1_data, section2_data, section3_data], axis=0).drop_duplicates().reset_index()

    department_data = professors.loc[:, ["Department", "Department Name"]].drop_duplicates().reset_index()

    professor_data = professors.loc[:, ["Name", "Age", "Gender", "Office", "Title", "Department", "Email"]]

    enrolls_data = students.loc[:, ["Full Name", "Courses 1", "Course 1 Section", "Courses 2", "Course 2 Section",
                                    "Courses 3", "Course 3 Section"]]

    prof_team_data = professors.loc[:, ["Team ID"]]

    prof_team_member_data = professors.loc[:, ["Name", "Team ID"]]

    homework_data1 = students.loc[:, ["Courses 1", "Course 1 Section", "Course 1 HW_No", "Course 1 HW_Details"]]
    homework_data1.columns = ["Course", "Section", "HW_No", "HW_Details"]
    homework_data2 = students.loc[:, ["Courses 2", "Course 2 Section", "Course 2 HW_No", "Course 2 HW_Details"]]
    homework_data2.columns = ["Course", "Section", "HW_No", "HW_Details"]
    homework_data3 = students.loc[:, ["Courses 3", "Course 3 Section", "Course 3 HW_No", "Course 3 HW_Details"]]
    homework_data3.columns = ["Course", "Section", "HW_No", "HW_Details"]
    homework_data = pd.concat([homework_data1, homework_data2, homework_data3], axis=0).drop_duplicates().reset_index()

    homework_grade_data = students.loc[:, ["Full Name", "Courses 1", "Course 1 Section", "Course 1 HW_No",
                                           "Course 1 HW_Grade", "Courses 2", "Course 2 Section", "Course 2 HW_No",
                                           "Course 2 HW_Grade", "Courses 3", "Course 3 Section", "Course 3 HW_No",
                                           "Course 3 HW_Grade"]]

    populate_users(user_data)
    popular_zipcodes(zipcode_data)
    populate_students(student_data)
    populate_courses(course_data)
    populate_departments(department_data)
    populate_professors(professor_data)
    populate_sections(section_data)
    populate_enrolls(enrolls_data)
    populate_prof_teams(prof_team_data)
    populate_prof_team_members(prof_team_member_data)
    populate_homeworks(homework_data)
    populate_homework_grades(homework_grade_data)

