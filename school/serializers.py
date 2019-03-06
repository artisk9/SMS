from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



#Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
	department = serializers.CharField(read_only=True)
	department_id = serializers.CharField(write_only=True)

	class Meta:
		model = Department
		fields = '__all__'


#School Serializer
class SchoolSerializer(serializers.ModelSerializer):
	class Meta:
		many = True
		model = School
		fields = ('name')

#Classes Serializer
class ClassesSerializer(serializers.ModelSerializer):
	teacher_id = serializers.CharField(write_only=True)
	subject_id = serializers.CharField(write_only=True)

	class Meta:
		many = True
		model = Classes
		fields = '__all__'


#Parent Serializer
class ParentSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username',read_only=True)
	first_name = serializers.CharField(source='user.first_name',read_only=True)
	last_name = serializers.CharField(source='user.last_name',read_only = True)
	email = serializers.CharField(source='user.email',read_only=True)
	password = serializers.CharField(source='user.password',read_only=True)

	class Meta:
			many = True
			model = Parent
			fields = '__all__'

#StudentProfile
class StudentProfileSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username',read_only=True)
	first_name = serializers.CharField(source='user.first_name',read_only=True)
	last_name = serializers.CharField(source='user.last_name',read_only = True)
	email = serializers.CharField(source='user.email',read_only=True)
	password = serializers.CharField(source='user.password',read_only=True)
	
	class Meta:
			many = True
			model = StudentProfile
			fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username',read_only=True)
	first_name = serializers.CharField(source='user.first_name',read_only=True)
	last_name = serializers.CharField(source='user.last_name',read_only=True)
	email = serializers.CharField(source='user.email',read_only=True)
	password = serializers.CharField(source='user.password',read_only=True)


	class Meta:
			many = True
			model = Teacher
			fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
			many = True
			model = Subject
			fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):

	studentprofile_first_name = serializers.CharField(source = 'studentprofile.user.first_name',read_only=True)
	studentprofile_last_name = serializers.CharField(source = 'studentprofile.user.last_name',read_only=True)
	teacher_first_name = serializers.CharField(source = 'teacher.user.first_name',read_only=True)
	teacher_last_name = serializers.CharField(source = 'teacher.user.last_name',read_only=True)
	subject_name = serializers.CharField(source = 'subject.name',read_only=True)
	attendance_status = serializers.CharField(source = 'attendance.attendance_status',read_only=True)

	class Meta:
			many = True
			model = Attendance
			fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
	class Meta:
			many = True
			model = Exam
			fields = '__all__'

class ExamSubjectMarkSerializer(serializers.ModelSerializer):
	student_mark_id = serializers.CharField(source= 'exam.id')
	studentprofile_first_name = serializers.CharField(source = 'studentprpfile.user.first_name',read_only=True)
	studentprofile_last_name = serializers.CharField(source='studentprofile.user.last_name',read_only=True)
	teacher_id = serializers.CharField(source = 'teacher.id',read_only=True)
	subject_marks_id = serializers.CharField(source= 'subject.id',read_only=True)

	class Meta:
			many = True
			model = ExamSubjectMark
			fields = '__all__'
