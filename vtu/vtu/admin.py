from django.contrib import admin

from .models import AdminEmailId,EmailConfig,FeedBackForm,MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterQuestionPapers,MasterVideoLab,AppForceUpdateRequired,AppVersion,DeviceAuth,MasterSyllabusCopy,MasterAbout


admin.site.register(MasterNotes)
admin.site.register(MasterBranches)
admin.site.register(MasterSemesters)
admin.site.register(MasterSubjects)
admin.site.register(MasterQuestionPapers)
admin.site.register(MasterVideoLab)
admin.site.register(AppForceUpdateRequired)
admin.site.register(AppVersion)
admin.site.register(DeviceAuth)
admin.site.register(MasterSyllabusCopy)
admin.site.register(MasterAbout)
admin.site.register(FeedBackForm)
admin.site.register(EmailConfig)
admin.site.register(AdminEmailId)
