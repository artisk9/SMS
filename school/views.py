from school.models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect # easy-to-use protection against attack
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser,FormParser
from django.contrib.auth import authenticate, login #login and authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import permission_required #check whether a user has a particular permission.


# Index Api
def index(request):
    return render(request,'school/home.html')

def attendance(request):
    return render(request,'school/attendance.html')

def subject(request):
    return render(request,'school/subject.html')

def studprofile(request):
	return render(request,'school/studentprofile.html')

def admission(request):
	return render(request, 'school/admission.html')



#registration Api
def register(request):
    if request.method == 'POST':
        form = RegistraionForm(request.POST )
        if form.is_valid:
            form.save()
            return redirect('/school')
    else:
        form = RegistraionForm()
        args ={form :'form'}
        return render(request,'school/register.html',args)
#Home Api
def home(request):
        school = school_school.objects.all()[:10]

        context = {
                'Username' : 'Username',
                'school' : 'school'
        }
        return render(request,'school/login.html',context)


# def login(request):
#     msg = []
#     if request.method == 'POST':
#         username = request.POST['u']
#         password = request.POST['p']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 auth_login(request, user)
#                 msg.append("login successful")
#             else:
#                 msg.append("disabled account")
#         else:
#             msg.append("invalid login")
#     return render_to_response('login.html', {'errors': msg})


def exam_marks(request):
	return render(request, "exam_marks.html")

def attendance(request):
	return render(request, "attendance.html")

#School Api
@csrf_exempt
@require_http_methods(["GET", "POST"])
def schoolApi(request):
	print request #priting output of request
	if user is not None and user.is_staff and user.is_superuser:
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username = username , password = password)
			serializer = SchoolSerializer(user, many=True)
			if serializer.is_valid():
				serializer.save()
			return JsonResponse(serializer.data)
		else:
			schoolData = School.objects.all()
			serializer = SchoolSerializer(schoolData,many=True)
			return JsonResponse(serializer.data,safe=False)
	return render(request,'school/school.html')

#DepartmentApi()
@csrf_exempt
@require_http_methods(["GET", "POST"])
def departmentApi(request):
	if request.method == 'GET':
		if 'name' in request.GET:
			department = Department.objects.filter(name=request.GET['name'])
		else:
			department = Department.objects.all()
		serializer = DepartmentSerializer(department, many=True)
		return JsonResponse(serializer.data,safe=False)
	elif request.method == 'POST':
		if 'name' in request.POST:
			data = {'name':request.POST['name']}
		else:
			return JsonResponse({'error': 'Please provide department name'},status=status.HTTP_400_BAD_REQUEST)
		serializer = DepartmentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

#classesApi
@csrf_exempt
@require_http_methods(["GET", "POST"])
def classesApi(request):
	if request.method == 'GET':
		if 'name' in  request.GET:
			classes = Classes.objects.filter(name=request.GET['name'])
		elif 'division' in request.GET:
			classes = Classes.objects.filter(request.GET['division'])
		else:
			classes = Classes.objects.all()
		serializer = ClassesSerializer(classes, many=True)
		return JsonResponse(serializer.data,safe=False)
	elif request.method == 'POST':
		if ('name' in request.POST and 'division' in request.POST and 'department_id' in request.POST) :
			data = {'name':request.POST['name'],'division':request.POST['division'],'department_id':request.POST['department_id']}
		else:
			return JsonResponse({'error': 'Please pass name, division, department_id'},status=status.HTTP_400_BAD_REQUEST)
		serializer = ClassesSerializer(data=data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

#Parent API
@csrf_exempt
@require_http_methods(["GET", "POST"])
def parentApi(request):
	if request.method == 'GET':
		if 'username' in request.GET:
			try:
				parents = Parent.objects.get(user = User.objects.get(username = request.GET['username']))
				serializer = ParentSerializer(parents)
				# student = Student.objects.filter(parent=)
				id = serializer.data['id']
				studentsData = StudentProfile.objects.filter(parent = id)
				studentSerializer = StudentProfileSerializer(studentsData,many=True)
				data = {'parent':serializer.data,'children':studentSerializer.data}
				return JsonResponse(data)
			except ObjectDoesNotExist:
				return JsonResponse({'error': 'No data found for user '+request.GET['username']},status=status.HTTP_200_OK)
		else:
			parents = Parent.objects.all()
			serializer = ParentSerializer(parents, many=True)
			return JsonResponse(serializer.data,safe=False)

	elif request.method == 'POST':
			if ('username' in request.POST and 'password' in request.POST and 'email' in request.POST and 'first_name' in request.POST and
				 'last_name' in request.POST and 'contact' in request.POST and 'address' in request.POST):
				user = User.objects.create_user(username = request.POST['username'],
					password = request.POST['password'],email = request.POST['email'],first_name = request.POST['first_name'],
					last_name = request.POST['last_name'])
				data = {'user':user.id,'contact':request.POST['contact'],'address':request.POST['address']}
			else:
				return JsonResponse({'error': 'Please enter name, division, department_id'},status=status.HTTP_400_BAD_REQUEST)
			serializer = ParentSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(serializer.data, status=201)
			return JsonResponse(serializer.errors, status=400)

	else:
		return JsonResponse({'error': 'You are not authorized to do this Operation'},status=status.HTTP_401_UNAUTHORIZED)




#Student Api
@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def studentProfileApi(request):
	if request.method == 'GET':
		if 'username' in request.GET:
			try: #to handle exception
				student = StudentProfile.objects.get(user = User.objects.get(username = request.GET['username']))
				serializer = StudentProfileSerializer(student)
				print(student)
			except ObjectDoesNotExist:
				return JsonResponse({'error': 'No data found for user '+request.GET['username']},status=status.HTTP_200_OK)
		else:
			student = StudentProfile.objects.all()
			serializer = StudentProfileSerializer(student, many=True)
		return JsonResponse(serializer.data,safe=False)

	elif request.method == 'POST':
		if ('username' in request.POST and 'password' in request.POST and 'email' in request.POST and 'first_name' in request.POST and
				 'last_name' in request.POST and 'contact' in request.POST and 'address' in request.POST and 'parent_id' in request.POST and 'classes_id' in request.POST):
				user = User.objects.create_user(username = request.POST['username'],
					password = request.POST['password'],email = request.POST['email'],first_name = request.POST['first_name'],
					last_name = request.POST['last_name'])
				data = {'user':user.id,'contact':request.POST['contact'],'address':request.POST['address'],'parent_id':parent_id,'classes_id':classes_id}
		else:
			return JsonResponse({'error': 'Please pass required fields'},status=status.HTTP_400_BAD_REQUEST)
			serializer = StudentProfileSerializer(data=data)
			if serializer.is_valid():

				serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	else:
	    return JsonResponse({'error': 'You are not authorized to do this Operation'},status=status.HTTP_401_UNAUTHORIZED)

#SubjectApi
@csrf_exempt
@require_http_methods(["GET", "POST"])
def subjectApi(request):
	if request.method == 'GET':
		#Check is user is Staff or Superuser
		if not request.user.is_staff or not request.user.is_superuser:
			return JsonResponse({'error':'You are not authorized to do this operation.'},status=status.HTTP_401_UNAUTHORIZED)
		if 'name' in request.GET:
			subject = Subject.objects.filter(name=request.GET['name'])
		else:
			subject = Subject.objects.all()
		serializer = SubjectSerializer(subject, many=True)
		return JsonResponse(serializer.data,safe=False)
	elif request.method == 'POST':
		if request.user.is_superuser:
			if ('name' in request.POST and 'classes_id' in request.POST and 'teacher_id' in request.POST) :
				data = {'name':request.POST['name'],
						'classes_id':request.POST['classes_id'],
						'teacher_id':request.POST['teacher_id']
						}
			else:
				return JsonResponse({'error': 'Please provide subject name'},
            		status=status.HTTP_400_BAD_REQUEST)
		else:
			return JsonResponse({'error':'You are not authorized to do this operation.'},status=status.HTTP_401_UNAUTHORIZED)
		serializer = SubjectSerializer(data=data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

#Exam Api
@csrf_exempt
@require_http_methods(["GET", "POST"])
def examApi(request):
	if request.method == 'GET':
		if 'title' in request.GET:
			exam = Exam.objects.filter(title=request.GET['title'])
		elif 'batch' in request.GET:
			exam = Exam.objects.filter(batch=request.GET['batch'])
		elif 'id' in request.GET:
			try:
				exam = Exam.objects.filter(classes = request.GET['id'])
			except ObjectDoesNotExist:
				return JsonResponse({'error': 'No data found for exam '+ request.GET['name']},status=status.HTTP_200_OK)
		else:
			exam = Exam.objects.all()
		serializer = ExamSerializer(exam, many=True)
		return JsonResponse(serializer.data,safe=False)

	elif request.method == 'POST':
		if ('title' in request.POST and 'batch' in request.POST and 'classes_id' in request.POST and 'teacher_id' in request.POST) :

			data = {'title':request.POST['title'],
					'batch':request.POST['batch'],
					'classes_id':request.POST['classes_id'],
					'teacher_id':request.POST['teacher_id']
					}
		else:
			return JsonResponse({'error': 'Please provide exam name'},status=status.HTTP_400_BAD_REQUEST)

		serializer = ExamSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def attendanceApi(request):
    if request.method == 'GET':
        if 'student_name' in request.GET and 'start_date' in request.GET and 'end_date' in request.GET:
            userData = User.objects.get(username = request.GET['student_name'])
            attendance = Attendance.objects.filter(student=Student.objects.get(user=userData),date__gte=request.GET['start_date'],date__lte=request.GET['end_date'])
            serializer = AttendanceSerializer(attendance,many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            attendance = Attendance.objects.all()
            serializer = AttendanceSerializer(attendance,many=True)
            return JsonResponse(serializer.data,safe=False)
        return JsonResponse({'error':'Please Provide Valid Data'}, status=status.HTTP_400_BAD_REQUEST)

#subjectMarksApi
@csrf_exempt
@require_http_methods(["GET", "POST"])
def subjectMarksApi(request):
    if request.method == 'GET':
        if 'student_name' in request.GET and 'title' in request.GET and 'year' in request.GET:
            userData = User.objects.get(username = request.GET['student_name'])
            student = Student.objects.get(user = userData)
            # classes = classes.objects.get(name = student.classes.name)
            exam = Exam.objects.filter(title = request.GET['title'],classes = student.classes)
            subjects = Subject.objects.filter(year = request.GET['year'])
            examSubject = ExamSubject.objects.filter(student = student,subject__in = [s.id for s in subjects], exam__in = [e.id for e in exam])
            serializer = ExamSubjectSerializer(examSubject,many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse({'error':'Please provide valid Data'},status=status.HTTP_400_BAD_REQUEST)
#End subjectMarksApi

#TeacherApi
@csrf_exempt
@require_http_methods({'GET','POST'})
def teacherApi(request):
	if user is not None and user.is_staff and user.is_superuser:
		if request.method == "GET":
			teacherData = Teacher.objects.all()
			serializer = TeacherSerializer(teacherData,many=True)
			return JsonResponse(serializer.data,safe = False)
		#	return render (request, '/subject.html',subjectMark)

	else:
			teacherData = Teacher.objects.filter()
			serializer = TeacherSerializer(teacherData,many=True)
			return JsonResponse(serializer.data,safe =False)
	return JsonResponse({'error':'Error'}, status = status.HttpResponseNotFound)


