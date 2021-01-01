from django.db import models
from django.contrib.auth.models import User


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