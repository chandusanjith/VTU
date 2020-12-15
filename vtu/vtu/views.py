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
from .models import MasterSemesters,MasterBranches,MasterNotes
from .serializers import NotesSerializer, NotesMasterSerializer
from rest_framework import parsers
from collections import namedtuple


class SnippetList(APIView):
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,) 
  serializer_class = NotesSerializer


  def get(self, request, sem, branch, format=None):
    ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
    ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
    Notes_raw = MasterNotes.objects.filter(semester = ws_semester, branch = ws_branch)
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
      
