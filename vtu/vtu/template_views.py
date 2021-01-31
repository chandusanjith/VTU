from .models import NewNotes,TrackNotesDownlods,OTPValidate,ContactUs,TermsAndConditions, AdminEmailId, EmailConfig,MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterServiceHits,MasterQuestionPapers, MasterVideoLab, DeviceAuth, AppVersion, AppForceUpdateRequired, MasterSyllabusCopy,MasterAbout
from django.contrib import admin
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .Autherizer import AuthRequired,AuthLink
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, auth




def LoadDashBoard(request):
    #dat = DeviceAuth.objects.annotate(month=TruncMonth('updated_on')).values('month').annotate(c=Count('device_key')).values('month', 'c')
    #dat = DeviceAuth.objects.all()
    dat = DeviceAuth.objects.all().extra({'date_created': "date(updated_on)"}).values('updated_on').annotate(created_count=Count('device_key'))
    authors_data = MasterAbout.objects.all()
    notes_count = MasterNotes.objects.all().count()
    qpaper_count = MasterQuestionPapers.objects.all().count()
    syllcopy_count = MasterSyllabusCopy.objects.all().count()
    LabManual_vidoes_added = MasterVideoLab.objects.all().count()
    apihits = MasterServiceHits.objects.all()
    terms  = TermsAndConditions.objects.all()
    admin1 = AdminEmailId.objects.filter(id=1).first()
    admin2 =  AdminEmailId.objects.filter(id=2).first()
    sys_email = EmailConfig.objects.filter(id=1).first()
    app_force_update = AppForceUpdateRequired.objects.filter(id=1).first()
    app_version = AppVersion.objects.filter(id=1).first()
    context={
        'device_data':dat,
        'authors_data':authors_data,
        'notes_count':notes_count,
        'syllcopy_count':syllcopy_count,
        'LabManual_vidoes_added':LabManual_vidoes_added,
        'qpaper_count':qpaper_count,
        'apihits':apihits,
        't_c':terms,
        'admin1':admin1.mail_reciever_email,
        'admin2': admin2.mail_reciever_email,
        'sys_email':sys_email.email_id,
        'app_force_update':app_force_update.force_update_required,
        'app_version':app_version.version,
    }
    return render(request, 'index.html', context)

def LoadPrivacyPolicy(request):
    return render(request, 'PrivacyPolicy.html')
def LoadAboutus(request):
    return render(request, 'AboutUs.html')
def LoadTerms(request):
    return render(request, 'Terms_of_use.html')
def ThankYou(request):
    return render(request,'ThankYou.html')
def UserNotesUpload(request, id, device_auth, link_mapper):
    if AuthRequired(device_auth) == True:
        contact_details = ContactUs.objects.filter(id=id).first()
        if AuthLink(contact_details.email,link_mapper) == True:
            if request.method == "GET":
                #contact_details = ContactUs.objects.filter(id=id).first()
                context = {
                    'name': contact_details.name,
                    'contact': contact_details.contact,
                    'email': contact_details.email,
                    'id':id,
                    'device_id':device_auth,
                    'mapped_id':link_mapper,
                }
                return render(request, 'userNotesUpload.html', context)
            else:
                name = request.POST['name']
                Description = request.POST['Description']
                notes = request.FILES["upnotes"]
                address = request.POST['address']
                email = request.POST['email']
                contact = request.POST['cnum']
                a = NewNotes(Description = Description,device_id = device_auth, notes = notes, name = name, email = email, contact = contact, address = address)
                a.save()
                return HttpResponseRedirect('/ThankYou/')
        else:
            return render(request, 'ReRegister.html')
    else:
        raise PermissionDenied


def NotesLogin(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/NotesMain/')
        else:
           return render(request, 'NotesLogin.html')
    else:
        uid = request.POST["uname"]
        password = request.POST["psw"]
        user = auth.authenticate(username=uid, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/NotesMain/')
        else:
            return HttpResponseRedirect('/NotesLogin/')

def NotesMain(request):
    newNotes = NewNotes.objects.filter(approved=False)
    context = {
        'newNotes':newNotes,
    }
    return render(request, 'NotesMain.html', context)



def NotesApprove(request, id):
    if request.method == "GET":
        newNotes = NewNotes.objects.filter(id=id).first()
        branches = MasterBranches.objects.all()
        semester = MasterSemesters.objects.all()
        context = {
            'newNotes': newNotes,
            'branches':branches,
            'semester':semester,
        }
        return render(request, 'NotesApprove.html', context)
