from django.urls import path, include
from django.http import HttpResponse, FileResponse
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
import json
from django.core import serializers
from .models import MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterQuestionPapers, MasterVideoLab, DeviceAuth, AppVersion, AppForceUpdateRequired, MasterSyllabusCopy,MasterAbout
from .serializers import NotesSerializer, NotesMasterSerializer, SubjectSerializer, QuestionPaperSerializer, MasterVideoLabSerializer, LoadSyllabusCopySerializer,MasterAboutSerializer
from rest_framework import parsers
from collections import namedtuple
from django.contrib import admin

import random
import string

class InitialLoad(APIView):

  def get(self, request, device_auth,format=None):
     if len(device_auth) != 16:
       return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)
     if DeviceAuth.objects.filter(device_key=device_auth).exists():
        app_version = AppVersion.objects.all()
        app_force_update = AppForceUpdateRequired.objects.all()
        mapped_key = DeviceAuth.objects.filter(device_key = device_auth)
        return Response({"Auth_key":mapped_key[0].mapped_key,
                        "app_version":app_version[0].version,
                        "app_force_update":app_force_update[0].force_update_required,
                        "user_type_old":"OLD_USER"}, status=status.HTTP_200_OK)
     else:
         mapped_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
         new_data = DeviceAuth(device_key=device_auth, mapped_key=mapped_id)
         new_data.save()
         app_version = AppVersion.objects.all()
         app_force_update = AppForceUpdateRequired.objects.all()
         mapped_key = DeviceAuth.objects.filter(device_key = device_auth)
         return Response({"Auth_key":mapped_key[0].mapped_key,
                        "app_version":app_version[0].version,
                        "app_force_update":app_force_update[0].force_update_required,
                        "user_type_new":"NEW_USER"}, status=status.HTTP_200_OK)


class SnippetList(APIView):
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,) 
  serializer_class = NotesSerializer


  def get(self, request, sem, branch, subject, device_auth,format=None):
    if AuthRequired(device_auth) == True:
      ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
      ws_subject = MasterSubjects.objects.filter(subject_name = subject).first()
      Notes_raw = MasterNotes.objects.filter(semester = ws_semester, branch = ws_branch, subject = ws_subject)
      if not Notes_raw:
        return Response({
          "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)
      notes_serializer = NotesSerializer(Notes_raw, many=True,context={'Device_key': device_auth}
).data
      return Response(notes_serializer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class QuestionPaperList(APIView):
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,) 
  serializer_class = QuestionPaperSerializer


  def get(self, request, sem, branch, subject, device_auth, format=None):
    if AuthRequired(device_auth) == True:
      ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
      ws_subject = MasterSubjects.objects.filter(subject_name = subject).first()
      Question_paper_raw = MasterQuestionPapers.objects.filter(semester = ws_semester, branch = ws_branch, subject = ws_subject)
      if not Question_paper_raw:
        return Response({
        "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)
      question_paper_serializer = QuestionPaperSerializer(Question_paper_raw, many=True,context={'Device_key': device_auth}
).data
      return Response(question_paper_serializer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)



class FetchMasterList(APIView):

  def get(self, request,device_auth, format=None):
    if AuthRequired(device_auth) == True:
      MasterRecords = namedtuple('MasterRecords', ('branches', 'semester'))
      master = MasterRecords(
              branches=MasterBranches.objects.all(),
              semester=MasterSemesters.objects.all(),
          )
      serializer = NotesMasterSerializer(master,context={'Device_key': device_auth}
).data
      return Response(serializer)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)
      
class FetchSubject(APIView):

  def get(self, request, sem, branch, device_auth, format=None):
    if AuthRequired(device_auth) == True:
      ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
      Sub_raw = MasterSubjects.objects.filter(subject_semester = ws_semester, subject_branch = ws_branch)
      if not Sub_raw:
        return Response({
        "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)
      sub_serializer = SubjectSerializer(Sub_raw, many=True,context={'Device_key': device_auth}
).data
      return Response(sub_serializer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)


class LabManualVid(APIView):
  def get(self, request, sem, branch, subject, program_id, device_auth, format=None):
    if AuthRequired(device_auth) == True:
      ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
      ws_subject = MasterSubjects.objects.filter(subject_name = subject).first()
      video_master = MasterVideoLab.objects.filter(semester=ws_semester,subject=ws_subject,branch=ws_branch,programid=program_id)
      if not video_master:
        return Response({
        "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)  
      video_serializer = MasterVideoLabSerializer(video_master, many=True,context={'Device_key': device_auth}
).data
      return Response(video_serializer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class LoadSyllabusCopy(APIView):
  def get(self, request, branch, device_auth, format=None):
    if AuthRequired(device_auth) == True:
      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
      syllabus_master = MasterSyllabusCopy.objects.filter(branch=ws_branch)
      if not syllabus_master:
        return Response({
        "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND) 
      syllabus_serilizer = LoadSyllabusCopySerializer(syllabus_master, many=True,context={'Device_key': device_auth}
).data
      return Response(syllabus_serilizer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class LoadAbout(APIView):
  def get(self, request, device_auth, format=None):
    if AuthRequired(device_auth) == True:
      about_master=MasterAbout.objects.all()
      if not about_master:
        return Response({
        "ERROR":"404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)
      about_serializer = MasterAboutSerializer(about_master, many=True, context={'Device_key': device_auth}
).data
      return Response(about_serializer, status=status.HTTP_200_OK)
    else:
      return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)    

def AuthRequired(auth_key):
    #testing git commit
  if len(auth_key) != 16:
    return False
  if DeviceAuth.objects.filter(device_key=auth_key).exists():
    return True
  else:
    return False 
