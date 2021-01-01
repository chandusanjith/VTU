from rest_framework import serializers
from .models import MasterNotes, MasterBranches, MasterSemesters, MasterSubjects, MasterQuestionPapers, MasterVideoLab


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterNotes
        fields = ('owner','file','Description','file_snippet','author')

class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterQuestionPapers
        fields = ('owner','file','Description','file_snippet')

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

class MasterVideoLabSerializer(serializers.ModelSerializer):
   class Meta:
     model = MasterVideoLab
     fields = '__all__' 