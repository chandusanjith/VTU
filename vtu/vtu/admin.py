from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea
from .models import OTPValidate,ContactUs,TermsAndConditions,AdminEmailId,EmailConfig,FeedBackForm,MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterQuestionPapers,MasterVideoLab,AppForceUpdateRequired,AppVersion,DeviceAuth,MasterSyllabusCopy,MasterAbout
from django.forms import Textarea

class TermsAndConditionsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'50'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


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
admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
admin.site.register(ContactUs)
admin.site.register(OTPValidate)