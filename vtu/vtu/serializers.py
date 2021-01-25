from rest_framework import serializers
from .models import PaymentPassBook,PaymentParameter,UserMoneyBucket,EmailUniqueidMapper,ContactUs,TermsAndConditions,FeedBackForm,MasterNotes, MasterBranches, MasterSemesters, MasterSubjects, MasterQuestionPapers, MasterVideoLab, MasterSyllabusCopy,MasterAbout,DeviceAuth


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

class NotesTrackerSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    Mapped_Key = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MasterNotes
        fields = ('id','Description','downloads','Mapped_Key','Auth_key')

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_Mapped_Key(self,request):
      mapped_key = self.context.get("Mapped_Key")
      return mapped_key

class PaymentSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    Mapped_Key = serializers.SerializerMethodField(read_only=True)
    Show_Redeem = serializers.SerializerMethodField(read_only=True)
    Redeem_api = serializers.SerializerMethodField(read_only=True)
    show_statement = serializers.SerializerMethodField(read_only=True)
    statement_api = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMoneyBucket
        fields = ('totAmountRedeemed','totAmountEarned','Show_Redeem','Redeem_api','show_statement','statement_api','Mapped_Key','Auth_key')

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key

    def get_Mapped_Key(self,request):
      mapped_key = self.context.get("Mapped_Key")
      return mapped_key

    def get_Show_Redeem(self, request):
        email = self.context.get("Email")
        moneyBucket = UserMoneyBucket.objects.filter(email=email).first()
        payment = PaymentParameter.objects.filter(id=1).first()
        if moneyBucket.totAmountEarned >= payment.minRedeemAmt:
            return True
        else:
            return False

    def get_Redeem_api(self, request):
        email = self.context.get("Email")
        mapped_key = self.context.get("Mapped_Key")
        Device_key = self.context.get("Device_key")
        moneyBucket = UserMoneyBucket.objects.filter(email=email).first()
        payment = PaymentParameter.objects.filter(id=1).first()
        if moneyBucket.totAmountEarned >= payment.minRedeemAmt:
            return 'apiv1/Redeem/'+mapped_key+'/'+Device_key
        else:
            return "N/A"

    def get_show_statement(self, request):
        email = self.context.get("Email")
        moneyBucket = UserMoneyBucket.objects.filter(email=email).first()
        payment = PaymentParameter.objects.filter(id=1).first()
        if PaymentPassBook.objects.filter(email=email).exists():
            return True
        else:
            return False

    def get_statement_api(self, request):
        email = self.context.get("Email")
        mapped_key = self.context.get("Mapped_Key")
        Device_key = self.context.get("Device_key")
        if PaymentPassBook.objects.filter(email=email).exists():
            return 'apiv1/Statement/'+mapped_key+'/'+Device_key
        else:
            return "N/A"

class TrackMasterSerializer(serializers.Serializer):
    NotesTrack = NotesTrackerSerializer(many=True)
    Earnings = PaymentSerializer(many=True)

class QuestionPaperSerializer(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MasterQuestionPapers
        fields = ('id','owner','file','type','Description','file_snippet','downloads','Auth_key')

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

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class TermsAndConditionsSerialier(serializers.ModelSerializer):
    Auth_key = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TermsAndConditions
        fields = '__all__'

    def get_Auth_key(self,request):
      Device_key = self.context.get("Device_key")
      mapped_key = DeviceAuth.objects.filter(device_key = Device_key)
      return mapped_key[0].mapped_key