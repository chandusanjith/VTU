from .models import TrackNotesDownlods,OTPValidate,ContactUs,TermsAndConditions, AdminEmailId, EmailConfig,MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterServiceHits,MasterQuestionPapers, MasterVideoLab, DeviceAuth, AppVersion, AppForceUpdateRequired, MasterSyllabusCopy,MasterAbout
from django.contrib import admin
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models.functions import ExtractMonth

def LoadDashBoard(request):
    dat = DeviceAuth.objects.annotate(month=TruncMonth('updated_on')).values('month').annotate(c=Count('device_key')).values('month', 'c')
    authors_data = MasterAbout.objects.all()
    notes_count = MasterNotes.objects.all().count()
    qpaper_count = MasterQuestionPapers.objects.all().count()
    syllcopy_count = MasterSyllabusCopy.objects.all().count()
    LabManual_vidoes_added = MasterVideoLab.objects.all().count()
    context={
        'device_data':dat,
        'authors_data':authors_data,
        'notes_count':notes_count,
        'syllcopy_count':syllcopy_count,
        'LabManual_vidoes_added':LabManual_vidoes_added,
        'qpaper_count':qpaper_count,
    }
    return render(request, 'index.html', context)

def LoadPrivacyPolicy(request):
    return render(request, 'PrivacyPolicy.html')
def LoadAboutus(request):
    return render(request, 'AboutUs.html')
def LoadTerms(request):
    return render(request, 'Terms_of_use.html')