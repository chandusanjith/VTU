from rest_framework import serializers
from .models import MasterNotes, MasterBranches, MasterSemesters


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterNotes
        fields = '__all__'
        depth = 1

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

