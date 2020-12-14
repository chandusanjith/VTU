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

class MasterNotes(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Notes_owner')
  semester = models.ForeignKey(MasterSemesters, on_delete=models.CASCADE, related_name='Semester_owner', null=True)
  branch = models.ForeignKey(MasterBranches, on_delete=models.CASCADE, related_name='Branch_owner', null=True)
  file = models.FileField(blank=True, null=True)
  Description = models.CharField(max_length=200, default=" ")
  Uploaded_on = models.DateField(auto_now_add=True)
