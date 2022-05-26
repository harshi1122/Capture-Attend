import json
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Student, Take_attendance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from json import dumps
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from .forms import CreateUserForm

import datetime
import xlwt
import datetime


@receiver(pre_delete, sender=Student)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.student_img.delete(False)

# Create your views here.
def index(request):
    return render(request, 'info/index.html')
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('home')
			

		context = {'form':form}
		return render(request, 'info/register.html', context)
# Login
@csrf_exempt
def handleLogin(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('add_student')
        else:
            messages.error(request, "Invalid Login")
            check=True
            return redirect('home')

# Logout 
def handleLogout(request):
    logout(request)
    return redirect('home')


# Marking attendance 
@login_required
def attendance(request):
    all_Student = Student.objects.all()
    # print(all_Student)
    # context = {'context':all_Student}
    # context = serializers.serialize('json', self.get_queryset())
    return render(request, 'info/attendance_new.html')


@csrf_exempt
def get_attendance(request):
    position = request.POST.get('position')
    if position=='All':
        position_data = Student.objects.all()
    else:
        position_data = Student.objects.filter(post=position)
   
    list_data = []

    for Stude in position_data:
        staff_sno = Student.objects.filter(name=Stude.name)[0]
      
        data_small = {"id": Stude.sno, "name": Stude.name, "post":Stude.post, "email":Stude.email}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Saving attendance Data 
@csrf_exempt
def save_data(request):
    if request.method == 'POST':
            Stude_ids = request.POST.get("Employe_ids")
            attendance_date = request.POST.get("attendance_date")
            section = request.POST.get("Section")
            print(section)
            json_Stude = json.loads(Stude_ids)
            print(json_Stude,attendance_date)
           
            if not Take_attendance.objects.filter(attendance_date=attendance_date,section=section).exists():
                
                try:
            # First Attendance Data is Saved on Attendance Model

                    for stud in json_Stude:

                        Stude = Student.objects.get(sno=stud['id'])
                        attendance_report = Take_attendance(name=Stude.name, status=stud['status'],university_roll=Stude.university_roll_no, attendance_date=attendance_date,section=section, employe=Stude)
                        attendance_report.save()
                    messages.success(request, "Attendance is added Successfully")
                    return HttpResponse("OK")
                except:
        
                    return HttpResponse("Error")
            else:
                # print("exist")
                return HttpResponse("Error")


# Adding Students Details 
@login_required
def add_student(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        university_roll_no = request.POST.get('university_roll_no', '')
        email = request.POST.get('email', '')
        position = request.POST.get('position', '')
        image = request.FILES['image']
    
        stude=Student(name=name, email=email, phone=phone,gender=gender, university_roll_no=university_roll_no, post=position, student_img=image)
       
        stude.save()
        messages.success(request, "Your message has been successfully sent")
    else:
        messages.success(request, 'Welcome to Add Student')
    return render(request, "info/add_student.html")


# Showing attendance Report 
@login_required
def attendance_report(request):
    messages.success(request, 'Welcome to Attendance Report')
    all_attendance= Take_attendance.objects.all()
   
    context = {'context':all_attendance}
    return render(request, "info/attendance_report.html", context)

#  Showing attendance of a particular date
@csrf_exempt
def admin_get_attendance(request):
    attendance_date = request.POST.get('attendance_date')
    section = request.POST.get('section')
    if section == "All":
        attendance_data = Take_attendance.objects.filter(attendance_date=attendance_date)
    else:
        attendance_data = Take_attendance.objects.filter(attendance_date=attendance_date,section=section)
 
    list_data = []

    for Stude in attendance_data:
        stud_sno = Student.objects.filter(name=Stude.name)[0]
 
        data_small={"id":Stude.sno, "name":Stude.name, "date":Stude.attendance_date, "status":Stude.status, "stud_sno":stud_sno.sno}
        list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@login_required
def all_student(request):
    return render(request, 'info/student_detail.html')


#  Showing Student Details
@login_required
def stud_details(request):
    sno = request.POST.get('staff_sno')
    detail = Student.objects.filter(sno=sno)[0]
    attendance_detail = Take_attendance.objects.filter(name=detail.name)

    list = []
    for data in attendance_detail:
        data_small={"name":data.name, "date":data.attendance_date, "status":data.status}
        list.append(data_small)

    return render(request, 'info/stud_details.html', {'detail':detail, 'attendance_detail':attendance_detail})

#  Searching attendance between two dates
@login_required
@csrf_exempt
def from_to_staff_attendance(request):
    date_from = request.POST.get('date_from')
  
    date_to = request.POST.get('date_to')
    Student_name = request.POST.get('Employe_name')
    get_data = Take_attendance.objects.filter(attendance_date__range=[date_from, date_to], name=Student_name)
   
    list = []
    for data in get_data:
        data_small = {"name": data.name, "date": data.attendance_date, "status": data.status}
        list.append(data_small)

    return JsonResponse(json.dumps(list), content_type="application/json", safe=False)

# Exporting attendance in Excel File
@login_required
@csrf_exempt
def export_excel(request):
    month = request.POST.get('month')
    year = request.POST.get('year')
    datetime_object = datetime.datetime.strptime(month, "%m")
    month_name = datetime_object.strftime("%b")
    section = request.POST.get('position')

    if month == '02':
        total_days = 29
    elif int(month) % 2 == 0 and int(month)<= 7:
        total_days = 31
    elif int(month) % 2 != 0 and int(month)>= 8:
        total_days = 31
    else :
        total_days = 32

# 1 2 3 4 5 6 7 8 9 10
# j f m a m j j a s o
# 1 8 1 0 1 0 1 1 0 1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=AttendenceData_' + \
        str(datetime.date.today())+'_'+ section+ '.xls' 
    wb = xlwt.Workbook(encoding='utf-8')  
    ws = wb.add_sheet('AttendenceData')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    i = 0
    
    ws.write(row_num, 0, 'Name', font_style)
    for col_num in range(1, total_days):
        ws.write(row_num, col_num, f'{col_num}-{month_name}-{year}', font_style)

    font_style = xlwt.XFStyle()

    
    
    # rows = Take_attendance.objects.all().values_list('name', 'date', 'status')
    if section=="All":
        rows = Student.objects.all().values_list('name')
    else:
        rows = Student.objects.filter(post=section).values_list('name')
    for name in rows:
        row_num += 1
        list = []
        dates = Take_attendance.objects.filter(attendance_date__range=[f'20{year}-{month}-01', f'20{year}-{month}-{total_days-1}'], name=f'{name[0]}')
        for data in dates:
            data_small = {"date": data.attendance_date, "status": data.status}
            list.append(data_small)
        ws.write(row_num, 0, f'{name[0]}', font_style)
        # print(list)
        for col_num in range(1, total_days):
            check = 0
            for l in list:
                if l['date'][8] == '0': # 2021-01-01
                    if l['date'] == f'20{year}-{month}-0{col_num}':
                        ws.write(row_num, col_num, f'{l["status"]}', font_style)
                        check = 1
                
                else:
                    if l['date'] == f'20{year}-{month}-{col_num}':
                        ws.write(row_num, col_num, f'{l["status"]}', font_style)
                        check = 1
            if check == 0:
                ws.write(row_num, col_num, f'NA', font_style)

    wb.save(response)

    return response
