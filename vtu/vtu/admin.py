from django.contrib import admin

from .models import MasterSemesters,MasterBranches,MasterNotes


admin.site.register(MasterNotes)
admin.site.register(MasterBranches)
admin.site.register(MasterSemesters)