from django.contrib import admin

from courses.models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Zipcode)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(Enrolls)