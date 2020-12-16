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
from .models import MasterSemesters,MasterBranches,MasterNotes, MasterSubjects
from .serializers import NotesSerializer, NotesMasterSerializer, SubjectSerializer
from rest_framework import parsers
from collections import namedtuple
from pdf2jpg import pdf2jpg
from django.contrib import admin


class SnippetList(APIView):
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,) 
  serializer_class = NotesSerializer


  def get(self, request, sem, branch, subject, format=None):
    ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
    ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
    ws_subject = MasterSubjects.objects.filter(subject_name = subject).first()
    Notes_raw = MasterNotes.objects.filter(semester = ws_semester, branch = ws_branch, subject = ws_subject)
    notes_serializer = NotesSerializer(Notes_raw, many=True)
    return Response(notes_serializer.data, status=status.HTTP_200_OK)

class FetchMasterList(APIView):

  def get(self, request, format=None):
    MasterRecords = namedtuple('MasterRecords', ('branches', 'semester'))
    master = MasterRecords(
            branches=MasterBranches.objects.all(),
            semester=MasterSemesters.objects.all(),
        )
    serializer = NotesMasterSerializer(master)
    return Response(serializer.data)
      
class FetchSubject(APIView):

  def get(self, request, sem, branch, format=None):
    ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
    ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
    Sub_raw = MasterSubjects.objects.filter(subject_semester = ws_semester, subject_branch = ws_branch)
    sub_serializer = SubjectSerializer(Sub_raw, many=True)
    return Response(sub_serializer.data, status=status.HTTP_200_OK)

