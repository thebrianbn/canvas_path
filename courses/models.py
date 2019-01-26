from django.db import models

# Create your models here.

class Users(models.Model):
    email_id = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Students(Users)
    pass


class Faculty(Users)
    pass


class Departments(models.Model):
    dept_id = models.CharField(max_length=25)
    dept_name = models.CharField(max_length=50)


class Courses(models.Model):
    course_id = models.CharField(max_length=25)
    course_name = models.CharField(max_length=50)
    #pre-requisites


class Sections(models.Model):
    section_num = models.CharField(max_length=25)

class CapstoneSection(Sections):
    pass
