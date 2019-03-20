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

    populate_users(user_data)
    popular_zipcodes(zipcode_data)
    populate_students(student_data)
    populate_courses(course_data)
    populate_departments(department_data)
    populate_professors(professor_data)
    populate_sections(section_data)
