from django.db import models
from django.contrib.auth.models import User

#School Model
class School(models.Model):
	name = models.CharField(max_length=100,unique=True)
	area = models.CharField(max_length=200)

	class Meta:
		db_table = 'school_school'

#Department Model- sem,marathi,english
class Department(models.Model):
	name = models.CharField(max_length=200,default='')

	class Meta:
		db_table = 'school_department'

#Classes Model
class Classes(models.Model):
	DIVISION_CHOICE =(('FirstShift','FirstShift'),
					  ('SecondShift','SecondShift'))

	name = models.CharField(max_length=100,default='')
	division = models.CharField(max_length=15,choices=DIVISION_CHOICE,default='')
	department = models.ForeignKey(Department,on_delete=models.CASCADE)

	class Meta:
		db_table = 'school_classes'


#Parent Model
class Parent(models.Model):
	name = models.CharField(max_length=200,default='')
	#user = models.ForeignKey(User, on_delete=models.CASCADE)
	contact = models.IntegerField()
	address = models.CharField(max_length=500,default='')


	class Meta:
		db_table = 'school_parent'


#StudentProfile Model
class StudentProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
	classes = models.ForeignKey(Classes,on_delete=models.CASCADE,null=True)
	contact = models.IntegerField()
	email = models.EmailField(max_length=254)
	parent = models.ForeignKey(Parent,on_delete=models.CASCADE,null=True)

	class Meta:
		db_table = 'school_studentprofile'


#Teacher Model
class Teacher(models.Model):
	CLASS_CHOICES=(('5th','5th'),
				 ('6th','6th'),
				 ('7th','7th'),
				 ('8th','8th'),
				 ('9th','9th'),
				 ('10th','10th'))
	name = models.CharField(max_length=200,default='')
	#user = models.ForeignKey(User, on_delete = models.CASCADE)
	department = models.ForeignKey(Department,on_delete = models.CASCADE)
	for_class = models.CharField(max_length=15,choices=CLASS_CHOICES)

	class Meta:
		db_table = 'school_teacher'

 #Subject Model
class Subject(models.Model):
	name = models.CharField(max_length=50, default='')
	classes = models.ForeignKey(Classes,on_delete= models.CASCADE)
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

	class Meta:
		db_table = 'school_subject'

# Attaendance Model
class Attendance(models.Model):
	ATTENDANCE_STATUS = (('P','Present'),
						 ('A','Absent'))
	student = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	date = models.DateTimeField()
	attendance_status = models.CharField(max_length=15, choices=ATTENDANCE_STATUS)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	remark = models.CharField(max_length=20,default='')

	class Meta:
		db_table = 'school_attendance'


#Exam Model
class Exam(models.Model):
	date = models.DateTimeField()
	title = models.CharField(max_length=80,default='')
	batch = models.CharField(max_length=80,default='')
	exam = models.ForeignKey(Classes , on_delete=models.CASCADE)

	class Meta:
		db_table = 'school_exam'


#ExamSubject Model
class ExamSubjectMark(models.Model):
	name = models.ForeignKey(StudentProfile,on_delete= models.CASCADE)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	student = models.ForeignKey(Classes, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	marks = models.FloatField()
	teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE)

	class Meta:
		db_table = 'school_examsubjectmark'







