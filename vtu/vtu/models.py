from django.db import models
from django.contrib.auth.models import User

FORCE_UPDATE_CHOICES = (
  ('YES', 'YES'),
  ('NO', 'NO'),
)

class MasterSemesters(models.Model):
  sem_name = models.CharField(max_length=200, unique=True)
  created_on = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.sem_name

class MasterBranches(models.Model):
  branch_name = models.CharField(max_length=200, unique=True)
  created_on = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return self.branch_name

class MasterSubjects(models.Model):
  subject_branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='Branch_subject', null=True)
  subject_semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='Semester_subject', null=True)
  subject_code = models.CharField(max_length=10, unique=True)
  subject_name = models.CharField(max_length=200, unique=True)
  Description = models.CharField(max_length=200, default=" ")
  Uploaded_on = models.DateField(auto_now_add=True)

  def __str__(self):
      return self.subject_name  

class MasterNotes(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Notes_owner')
  owner_email = models.CharField(max_length=60, default=" ")
  semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='Semester_owner', null=True)
  branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='Branch_owner', null=True)
  author = models.CharField(max_length=40, default=" ")
  subject = models.ForeignKey(MasterSubjects, on_delete=models.CASCADE, related_name='Master_owner', null=True)
  file = models.FileField(blank=True, null=True)
  file_snippet = models.FileField(blank=True, null=True)
  Description = models.CharField(max_length=200, default=" ")
  Uploaded_on = models.DateField(auto_now_add=True)
  downloads = models.IntegerField(default=0)

  def __str__(self):
      return self.Description 


class MasterQuestionPapers(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_question')
  semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='Semester_question', null=True)
  branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='Branch_question', null=True)
  subject = models.ForeignKey(MasterSubjects, on_delete=models.CASCADE, related_name='Master_question', null=True)
  file = models.FileField(blank=True, null=True)
  file_snippet = models.FileField(blank=True, null=True)
  Description = models.CharField(max_length=200, default=" ")
  Uploaded_on = models.DateField(auto_now_add=True)
  downloads = models.IntegerField(default=0)

  def __str__(self):
      return self.Description

class MasterProgramId(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_question')
  semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='id_question', null=True)
  branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='id_question', null=True)
  subject = models.ForeignKey(MasterSubjects, on_delete=models.CASCADE, related_name='id_question', null=True)  
  programid = models.IntegerField(default=0)


class MasterVideoLab(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videolab_owner')
  semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='videolab_question', null=True)
  subject = models.ForeignKey(MasterSubjects, on_delete=models.CASCADE, related_name='videolab_question', null=True)
  branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='videolab_question', null=True)
  programid = models.IntegerField(default=0)
  title = models.CharField(max_length=200, default=" ")
  video = models.FileField(blank=True, null=True)
  views = models.IntegerField(default=0)
  description = models.CharField(max_length=400, default=" ")
  thumbnail = models.FileField(blank=False, null=True)

  def __str__(self):
      return self.title

class DeviceAuth(models.Model):
  device_key = models.CharField(max_length=16, default=" ")
  mapped_key = models.CharField(max_length=16, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
      return self.device_key

class AppVersion(models.Model):
  version = models.CharField(max_length=16, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
      return self.version


class AppForceUpdateRequired(models.Model):
  force_update_required =  models.CharField(choices=FORCE_UPDATE_CHOICES, max_length=3)

  def __str__(self):
    return self.force_update_required

class MasterSyllabusCopy(models.Model):
  branch=models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='syllabus_branch', null=True)
  title = models.CharField(max_length=40, default=" ")
  file = models.FileField(blank=True, null=True)
  updated_on = models.DateField(auto_now_add=True)
  downloads = models.IntegerField(default=0)

  def __str__(self):
    return self.title

class MasterAbout(models.Model):
  app_name=models.CharField(max_length=40, default=" ")
  header=models.CharField(max_length=40, default=" ")
  version = models.CharField(max_length=40, default=" ")
  description=models.CharField(max_length=100, default=" ")
  about_us_url=models.CharField(max_length=500, default=" ")
  terms_url=models.CharField(max_length=500, default=" ")
  privacy_url=models.CharField(max_length=500, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.app_name

class MasterServiceHits(models.Model):
  notes_hit = models.IntegerField(default=0)
  syllabus_copy_hit = models.IntegerField(default=0)
  question_paper_hit = models.IntegerField(default=0)
  lab_manual_video_hit = models.IntegerField(default=0)

  def __str__(self):
    return self.notes_hit + self.syllabus_copy_hit + self.question_paper_hit + self.lab_manual_video_hit

class FeedBackForm(models.Model):
  device_id = models.CharField(max_length=16, default="", null=False)
  name = models.CharField(max_length=50, default="",null=False)
  email = models.CharField(max_length=50, default="")
  contact_number = models.CharField(max_length=15, default="")
  feed_back = models.CharField(max_length=1000, default="", null=False)
  added_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.name

class EmailConfig(models.Model):
  email_id = models.CharField(max_length=50, default="", null=False)
  password = models.CharField(max_length=30, default="", null=False)

  def __str__(self):
    return self.email_id

class AdminEmailId(models.Model):
  mail_reciever_email = models.CharField(max_length=50, default="", null=False)
  added_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.mail_reciever_email

class TermsAndConditions(models.Model):
  title = models.CharField(max_length=40, default=" ")
  terms = models.TextField(max_length=1000, default=" ")
  added_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.title

class ContactUs(models.Model):
  name = models.CharField(max_length=40, default=" ")
  email = models.CharField(max_length=40, default=" ")
  contact = models.CharField(max_length=15, default=" ")
  device_id =  models.CharField(max_length=16, default=" ")
  user_message = models.CharField(max_length=1000, default=" ")
  user_verified = models.BooleanField(default=False)
  added_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.name

class OTPValidate(models.Model):
  device_id = models.CharField(max_length=16, default=" ")
  otp = models.IntegerField(default=0)
  email = models.CharField(max_length=40, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.device_id + str(self.otp)

class TrackNotesDownlods(models.Model):
  device_id = models.CharField(max_length=16, default=" ")
  notes_id = models.IntegerField(default=0)
  download_count = models.IntegerField(default=0)
  date = models.DateField()

  def __str__(self):
    return self.device_id + str(self.notes_id) + str(self.download_count)

class NewNotes(models.Model):
  device_id = models.CharField(max_length=16, default=" ")
  notes =  models.FileField(blank=True, null=True)
  name = models.CharField(max_length=40, default=" ")
  email = models.CharField(max_length=40, default=" ")
  contact = models.CharField(max_length=15, default=" ")
  address = models.CharField(max_length=240, default=" ")
  Description = models.CharField(max_length=240, default=" ")

  def __str__(self):
    return self.name

class EmailUniqueidMapper(models.Model):
  email = models.CharField(max_length=40, default=" ")
  mapped_id = models.CharField(max_length=16, default=" ")
  link_mapper = models.CharField(max_length=16, default=" ")
  link_expiry = models.DateField()

  def __str__(self):
    return self.email + '-' + self.mapped_id

class TrackerOTPValidate(models.Model):
  otp = models.IntegerField(default=0)
  email = models.CharField(max_length=40, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.email + '-' + self.otp

class PaymentNotesDownloadTracker(models.Model):
  notesID = models.IntegerField(default=0)
  initialViews = models.IntegerField(default=0)
  maxViews = models.IntegerField(default=0)
  updated_on = models.DateField(auto_now_add=True)

class PaymentParameter(models.Model):
  notesInitialAmt = models.DecimalField(max_digits=12, decimal_places=2)
  totEligibleViews = models.IntegerField(default=0)
  eligibleViewsAmt = models.DecimalField(max_digits=12, decimal_places=2)
  validViews = models.IntegerField(default=0)
  minRedeemAmt = models.DecimalField(max_digits=12, decimal_places=2)
  updated_on = models.DateField(auto_now_add=True)

class UserMoneyBucket(models.Model):
  email = models.CharField(max_length=40, default=" ")
  totAmountEarned = models.DecimalField(max_digits=12, decimal_places=2)
  totAmountRedeemed = models.DecimalField(max_digits=12, decimal_places=2)

class PaymentPassBook(models.Model):
  email = models.CharField(max_length=40, default=" ")
  credit = models.DecimalField(max_digits=12, decimal_places=2)
  debit = models.DecimalField(max_digits=12, decimal_places=2)
  currBalance = models.DecimalField(max_digits=12, decimal_places=2)
  narration = models.CharField(max_length=400, default=" ")
  tranDate = models.DateField(auto_now_add=True)

class GLAccount(models.Model):
  account = models.CharField(max_length=40, default=" ")
  balance = models.DecimalField(max_digits=12, decimal_places=2)
  updated_on = models.DateField(auto_now_add=True)

class GLPassBook(models.Model):
  account = models.CharField(max_length=40, default=" ")
  credit = models.DecimalField(max_digits=12, decimal_places=2)
  debit = models.DecimalField(max_digits=12, decimal_places=2)
  currBalance = models.DecimalField(max_digits=12, decimal_places=2)
  narration = models.CharField(max_length=400, default=" ")
  tranDate = models.DateField(auto_now_add=True)