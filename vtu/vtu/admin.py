from django.contrib import admin

from .models import MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterQuestionPapers


admin.site.register(MasterNotes)
admin.site.register(MasterBranches)
admin.site.register(MasterSemesters)
admin.site.register(MasterSubjects)
admin.site.register(MasterQuestionPapers)