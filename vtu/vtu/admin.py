from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea
from .models import *
from django.forms import Textarea

class TermsAndConditionsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'50'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class MasterNotesAdmin(admin.ModelAdmin):
    list_display = ('id','owner', 'owner_email','semester', 'branch','author', 'subject','file', 'file_snippet','Description', 'downloads',)
    list_filter = (
        ('subject', admin.RelatedOnlyFieldListFilter),
    )


admin.site.register(EmailUniqueidMapper)
admin.site.register(PaymentPassBook)
#admin.site.register(MasterNotes)
admin.site.register(PaymentNotesDownloadTracker)
admin.site.register(PaymentParameter)
admin.site.register(UserMoneyBucket)
admin.site.register(MasterNotes, MasterNotesAdmin)
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
admin.site.register(NewNotes)