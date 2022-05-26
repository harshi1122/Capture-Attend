from django.contrib import admin
from django.urls import path
from . import views
from . import face_recog

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.registerPage, name="register"),
    path('add_student/', views.add_student, name='add_student'),
    path('attendance/', views.attendance, name='attendance'),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('save_data/', views.save_data, name="save_data"),
    path('attendance_report/', views.attendance_report, name="attendance_report"),
    path('admin_get_attendance/', views.admin_get_attendance, name="admin_get_attendance"),
    path('get_attendance/', views.get_attendance, name="get_attendance"),
    path('stud_details/', views.stud_details, name="stud_details"),
    path('all_student/', views.all_student, name="all_student"),
    path('from_to_staff_attendance/', views.from_to_staff_attendance, name="from_to_staff_attendance"),
    path('export_excel/', views.export_excel, name="export_excel"),
    path('face_recog/',face_recog.face, name="face_recog")

]
