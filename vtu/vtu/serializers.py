from rest_framework import serializers
from .models import FeedBackForm,MasterNotes, MasterBranches, MasterSemesters, MasterSubjects, MasterQuestionPapers, MasterVideoLab, MasterSyllabusCopy,MasterAbout,DeviceAuth


class NotesSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MasterNotes
        fields = ('id','owner','file','type','Description','file_snippet','author','downloads','Auth_key')
    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_type(self, request):
        return "Notes"

class QuestionPaperSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MasterQuestionPapers
        fields = ('id','owner','file','Description','file_snippet','downloads','Auth_key')

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_type(self, request):
        return "Qpaper"

class SubjectSerializer(serializers.ModelSerializer):
  Auth_key = serializers.SerializerMethodField(read_only=True)
  class Meta:
      model = MasterSubjects
      fields = '__all__'

  def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

class BranchesSerilizer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    class Meta:
      model = MasterBranches
      fields = '__all__'

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

class SemesterSerilizer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    class Meta:
      model = MasterSemesters
      fields = '__all__'

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

class NotesMasterSerializer(serializers.Serializer):
    semester = SemesterSerilizer(many=True)
    branches = BranchesSerilizer(many=True)       

class MasterVideoLabSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta:
      model = MasterVideoLab
      fields = '__all__' 

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_type(self, request):
        return "LabVid"

class LoadSyllabusCopySerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta:
      model = MasterSyllabusCopy
      fields = '__all__'
      
    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_type(self,request):
        return "SBcopy"

class MasterAboutSerializer(serializers.ModelSerializer):

    Auth_key = serializers.SerializerMethodField(read_only=True)

    class Meta:
      model = MasterAbout
     #fields = ('name','designation','about','Auth_key')
      fields='__all__'

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackForm
        fields = '__all__'
