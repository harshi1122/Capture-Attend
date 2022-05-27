from multiprocessing import process
from unicodedata import name
import face_recognition as fr
import cv2
import numpy as np
from django.db.models import Q
import os
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Student, Take_attendance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
import pyttsx3

speech = pyttsx3.init()
speech.setProperty("rate",140)

def face(request):

    known_face_encodings = []
    known_face_names = []

    profiles = Student.objects.all()
    for profile in profiles:
        x = profile.name
        person = profile.student_img
        image_of_person = fr.load_image_file(f'media/{person}')
        person_face_encoding = fr.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{x}')


    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = fr.compare_faces(
                    known_face_encodings, face_encoding)
                name1 = "Unknown"

                face_distances = fr.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name1 = known_face_names[best_match_index]
                    print(name1)

                    if Student.objects.filter(name=name1).exists():
                        data = Student.objects.get(name=name1)
                        print(data)
                        now = date.today()
                        print(now)
                        if not Take_attendance.objects.filter(attendance_date=now, university_roll=data.university_roll_no).exists():
                            attendance_report = Take_attendance(name=name1, status="Present",university_roll=data.university_roll_no, attendance_date=now, section=data.post, employe=data)
                            attendance_report.save()
                face_names.append(name1)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name1 in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(frame, (left, bottom - 35),(right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name1.upper(), (left + 6, bottom - 6), font, 0.5, (0, 0, 0))

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, "info/attendance_new.html")