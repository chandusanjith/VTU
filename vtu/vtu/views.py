from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
import json
from django.core import serializers
from .models import *
from .serializers import *
from rest_framework import parsers
from collections import namedtuple
from django.contrib import admin
from django.db.models import Count
from django.db.models import F
from .automaticmail import SendEmail
from .OTPGenerator import GenerateOTP
from .Autherizer import AuthRequired
from .monetize import MonetizeNotes
from datetime import date
import random
import string

class InitialLoad(APIView):

  def get(self, request, device_auth,format=None):
     if len(device_auth) != 16:
       return Response({"ERROR":"Access Denied"}, status=status.HTTP_404_NOT_FOUND)
     if DeviceAuth.objects.filter(device_key=device_auth).exists():
        app_version = AppVersion.objects.filter(id=1).first()
        app_force_update = AppForceUpdateRequired.objects.filter(id=1).first()
        mapped_key = DeviceAuth.objects.filter(device_key = device_auth).first()
        print(mapped_key.updated_on)
        return Response({"Auth_key":mapped_key.mapped_key,
                        "app_version":app_version.version,
                        "app_force_update":app_force_update.force_update_required,
                        "user_type_old":"OLD_USER"}, status=status.HTTP_200_OK)
     else:
         mapped_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
         new_data = DeviceAuth(device_key=device_auth, mapped_key=mapped_id)
         new_data.save()
         app_version = AppVersion.objects.filter(id=1).first()
         app_force_update = AppForceUpdateRequired.objects.filter(id=1).first()
         mapped_key = DeviceAuth.objects.filter(device_key = device_auth).first()
         #print(mapped_key.updated_on)
         return Response({"Auth_key":mapped_key.mapped_key,
                        "app_version":app_version.version,
                        "app_force_update":app_force_update.force_update_required,
                        "user_type_new":"NEW_USER"}, status=status.HTTP_200_OK)


class SnippetList(APIView):
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,) 
  serializer_class = NotesSerializer


  def get(self, request, sem, branch, subject, device_auth,format=None):
    if AuthRequired(device_auth) == True:
      MasterServiceHits.objects.filter(id=1).update(notes_hit=F('notes_hit') + 1)
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
      MasterServiceHits.objects.filter(id=1).update(question_paper_hit=F('question_paper_hit') + 1)
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
      MasterServiceHits.objects.filter(id=1).update(lab_manual_video_hit=F('lab_manual_video_hit') + 1)
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
      MasterServiceHits.objects.filter(id=1).update(syllabus_copy_hit=F('syllabus_copy_hit') + 1)
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

class TrackDownloads(APIView):
    def get(self, request, type, id, device_auth, format=None):
        if AuthRequired(device_auth) == True:
            mapped_key = DeviceAuth.objects.filter(device_key=device_auth)
            if type == 'Notes':
                if TrackNotesDownlods.objects.filter(device_id=device_auth, notes_id=id).exists():
                    data = TrackNotesDownlods.objects.filter(device_id=device_auth, notes_id=id).first()
                    if data.date == date.today() and data.download_count < 10:
                        MasterNotes.objects.filter(id=id).update(downloads=F('downloads') + 1)
                        TrackNotesDownlods.objects.filter(notes_id=id,device_id=device_auth ).update(download_count=F('download_count') + 1)
                        MonetizeNotes(id)
                    elif data.date != date.today():
                        TrackNotesDownlods.objects.filter(notes_id=id, device_id=device_auth ).update(date=date.today())
                        TrackNotesDownlods.objects.filter(notes_id=id,device_id=device_auth ).update(download_count=1)
                        MasterNotes.objects.filter(id=id).update(downloads=F('downloads') + 1)
                        MonetizeNotes(id)
                else:
                    tracker = TrackNotesDownlods(device_id=device_auth, notes_id=id,download_count = 1,date = date.today() )
                    tracker.save()
                    MasterNotes.objects.filter(id=id).update(downloads=F('downloads') + 1)
                    MonetizeNotes(id)
                return Response({"status":"O.K"}, status=status.HTTP_200_OK)
            elif type == 'Qpaper':
                MasterQuestionPapers.objects.filter(id=id).update(downloads=F('downloads') + 1)
                return Response({"status": "O.K"}, status=status.HTTP_200_OK)
            elif type == 'SBcopy':
                MasterSyllabusCopy.objects.filter(id=id).update(downloads=F('downloads') + 1)
                return Response({"status": "O.K"}, status=status.HTTP_200_OK)
            elif type == 'LabVid':
                MasterVideoLab.objects.filter(id=id).update(views=F('views') + 1)
                return Response({"status": "O.K"}, status=status.HTTP_200_OK)
            else:
                return Response({"ERROR":"OOPS! an internal error occured :("}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class FeedBack(APIView):
    def post(self, request, format=None):
        if AuthRequired(request.data['device_id']) == True:
            serializer = FeedBackSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                admin_emails = AdminEmailId.objects.all()
                context = {
                    'name': request.data['name'],
                    'feedback': request.data['feed_back'],
                    'device_id': request.data['device_id'],
                }
                subject = 'FeedBack has been given by ' + ' ' + request.data['name']
                for reciever_mail in admin_emails:
                    mail_value = SendEmail(reciever_mail.mail_reciever_email , context,subject, 'FeedBackMail.html')
                if mail_value == True:
                    return Response({"status": "O.K"}, status=status.HTTP_200_OK)
                else:
                    return Response({"ERROR": "OOPS! an internal error occured :("}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"ERROR": "Form is not valid :("}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class LoadFeedBack(APIView):
    def get(self, request, device_auth, format=None):
        if AuthRequired(device_auth) == True:
            ws_terms = TermsAndConditions.objects.filter(id=1)
            if not ws_terms:
                return Response({
                    "ERROR": "404 NO DATA FOUND :("}, status=status.HTTP_404_NOT_FOUND)
            terms_serializer = TermsAndConditionsSerialier(ws_terms, many=True, context={'Device_key': device_auth}
                                                 ).data
            return Response(terms_serializer, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class ContactUS(APIView):

    def post(self, request, format=None):
        if AuthRequired(request.data['device_id']) == True:
            if ContactUs.objects.filter(device_id = request.data['device_id']).exists():
                old_contact_data = ContactUs.objects.filter(device_id = request.data['device_id']).first()
                if old_contact_data.email != request.data['email']:
                    ContactUs.objects.filter(device_id=request.data['device_id']).update(user_verified = False)
                ContactUs.objects.filter(device_id=request.data['device_id']).update(name=request.data['name'],
                                                                                     email=request.data['email'],
                                                                                     contact=request.data['contact'],
                                                                                     user_message=request.data['user_message'])
                if ContactUs.objects.filter(device_id = request.data['device_id'], user_verified = False):
                    response = GenerateOTP(request.data['device_id'],request.data['email'], request.data['name'], 'C')
                    if response == True:
                        return Response({"status": "OTP has been shared"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"ERROR": "OOPS! an internal error occured :("},
                                            status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"status": "User has been verified, no need of otp validation"}, status=status.HTTP_200_OK)
            else:
                serializer = ContactUsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                response = GenerateOTP(request.data['device_id'], request.data['email'], request.data['name'], 'C')
                if response == True:
                    return Response({"status": "OTP has been shared"}, status=status.HTTP_200_OK)
                else:
                    return Response({"ERROR": "OOPS! an internal error occured :("},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class ValidateOTP(APIView):
    def get(self, request, otp, device_auth, format=None):
        if AuthRequired(device_auth) == True:
            otp_inside = OTPValidate.objects.filter(device_id=device_auth).first()
            if otp == str(otp_inside.otp):
                ContactUs.objects.filter(device_id = device_auth, email = otp_inside.email).update(user_verified = True)
                contact_details = ContactUs.objects.filter(device_id = device_auth, email = otp_inside.email).first()
                link = 'http://34.219.72.32/UserNotesUpload/'+str(contact_details.id)+'/'+contact_details.device_id
                context = {
                    'name':contact_details.name,
                    'contact': contact_details.contact,
                    'email':otp_inside.email,
                    'message':contact_details.user_message,
                    'link':link,
                }
                subject = 'Thanks for contacting us!'
                mail_status = SendEmail(otp_inside.email, context, subject, 'ThanksForContactingUs.html')
                if mail_status == False:
                    return Response({"ERROR": "OOPS! an internal error occured :("}, status=status.HTTP_404_NOT_FOUND)
                subject = "Some user has contacted us!!!"
                admin_emails = AdminEmailId.objects.all()
                for reciever_mail in admin_emails:
                    mail_status = SendEmail(reciever_mail.mail_reciever_email, context, subject, 'ThanksForContactingUs.html')
                    if mail_status == False:
                        return Response({"ERROR": "OOPS! an internal error occured :("},
                                        status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"status": "O.K"}, status=status.HTTP_200_OK)
            else:
                #ContactUs.objects.filter(device_id=device_auth, email=otp_inside.email).delete()
                return Response({"status":"OTP not matching"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class NotesTracker(APIView):
    def get(self, request, type, email_uniqueid, device_auth, format=None):
        if AuthRequired(device_auth) == True:
            if type == 'OLD':
                unique_id = email_uniqueid
                if EmailUniqueidMapper.objects.filter(mapped_id = unique_id).exists():
                    mappedData = EmailUniqueidMapper.objects.filter(mapped_id = unique_id).first()
                else:
                    return Response({"ERROR": "REAuth required :("},
                                    status=status.HTTP_404_NOT_FOUND)
                email = mappedData.email
                TrackerRecords = namedtuple('TrackerRecords', ('NotesTrack', 'Earnings'))
                Tracker = TrackerRecords(
                    NotesTrack=MasterNotes.objects.filter(owner_email = email),
                    Earnings=UserMoneyBucket.objects.filter(email = email),
                )
                if not Tracker:
                    return Response({"ERROR":"404 NO DATA FOUND :(",
                                     "Mapped_key": unique_id}, status=status.HTTP_404_NOT_FOUND)
                #serializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth}
                                                   #).data
                notesTrackerSerializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth,
                                                                                 'Mapped_Key': unique_id,
                                                                                 'Email': email}).data
                return Response(notesTrackerSerializer, status=status.HTTP_200_OK)
            elif type == "NEW":
                email = email_uniqueid
                response = GenerateOTP(device_auth, email, "user", "N")
                if response == True:
                    return Response({"status": "OTP has been shared"}, status=status.HTTP_200_OK)
                else:
                    return Response({"ERROR": "OOPS! an internal error occured :("},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"ERROR": "OOPS! an internal error occured :("},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)

class TrackerOTPValidater(APIView):
    def get(self, request, otp, email, device_auth, format=None):
        if AuthRequired(device_auth) == True:
            otp_inside = TrackerOTPValidate.objects.filter(email=email).first()
            if otp == str(otp_inside.otp):
                mapped_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
                if EmailUniqueidMapper.objects.filter(email = email).exists():
                    EmailUniqueidMapper.objects.filter(email=email).update(mapped_id=mapped_id)
                else:
                    mappedData = EmailUniqueidMapper(mapped_id=mapped_id, email=email)
                    mappedData.save()
                TrackerRecords = namedtuple('TrackerRecords', ('NotesTrack', 'Earnings'))
                Tracker = TrackerRecords(
                    NotesTrack=MasterNotes.objects.filter(owner_email=email),
                    Earnings=UserMoneyBucket.objects.filter(email=email),
                )
                if not Tracker:
                    return Response({"ERROR": "404 NO DATA FOUND :(",
                                     "Mapped_key": mapped_id}, status=status.HTTP_404_NOT_FOUND)
                # serializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth}
                # ).data
                notesTrackerSerializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth,
                                                                                 'Mapped_Key': mapped_id,
                                                                                 'Email': email}).data
                return Response(notesTrackerSerializer, status=status.HTTP_200_OK)
            else:
                return Response({"status": "OTP not matching"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)