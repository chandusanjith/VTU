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
  name=models.CharField(max_length=40, default=" ")
  designation=models.CharField(max_length=40, default=" ")
  about=models.CharField(max_length=80, default=" ")
  updated_on = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.designation

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
  feed_back = models.CharField(max_length=200, default="", null=False)
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