from django.contrib import admin

from .models import MasterSemesters,MasterBranches,MasterNotes, MasterSubjects


admin.site.register(MasterNotes)
admin.site.register(MasterBranches)
admin.site.register(MasterSemesters)
admin.site.register(MasterSubjects)