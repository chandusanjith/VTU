from rest_framework import serializers
from .models import MasterNotes, MasterBranches, MasterSemesters, MasterSubjects


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterNotes
        fields = ('owner','file','Description')

class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
      model = MasterSubjects
      fields = '__all__'

class BranchesSerilizer(serializers.ModelSerializer):
   class Meta:
     model = MasterBranches
     fields = '__all__'

class SemesterSerilizer(serializers.ModelSerializer):
   class Meta:
     model = MasterSemesters
     fields = '__all__'

class NotesMasterSerializer(serializers.Serializer):
    semester = SemesterSerilizer(many=True)
    branches = BranchesSerilizer(many=True)       

