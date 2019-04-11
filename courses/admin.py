from django.contrib import admin

from courses.models import *

# admin models
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Zipcode)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(Enrolls)
admin.site.register(ProfTeams)
admin.site.register(ProfTeamMember)
admin.site.register(Homework)
admin.site.register(HomeworkGrade)
admin.site.register(Exam)
admin.site.register(ExamGrade)
