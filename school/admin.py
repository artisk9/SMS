
from django.contrib import admin
from school.models import *

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(Department)
admin.site.register(ExamSubjectMark)
admin.site.register(Exam) 
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Classes)
admin.site.register(School)