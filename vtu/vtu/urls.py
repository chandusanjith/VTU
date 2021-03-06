"""vtu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from vtu import views, template_views, monetize
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='VTU Free Notes API Documentation')


urlpatterns = [
    path('swagger/apiv1/Doc', schema_view),
    path('admin/', admin.site.urls),
    path('apiv1/InitialLoad/<device_auth>', views.InitialLoad.as_view()),
    path('apiv1/LoadMasterData/<device_auth>', views.FetchMasterList.as_view()),
    path('apiv1/Notes/<sem>/<branch>/<subject>/<device_auth>', views.SnippetList.as_view()),
    path('apiv1/Subjects/<sem>/<branch>/<device_auth>',views.FetchSubject.as_view() ),
    path('apiv1/QP/<sem>/<branch>/<subject>/<device_auth>', views.QuestionPaperList.as_view()),
    path('apiv1/LabVid/<sem>/<branch>/<subject>/<program_id>/<device_auth>', views.LabManualVid.as_view()),
    path('apiv1/LoadSyllabusCopy/<branch>/<device_auth>', views.LoadSyllabusCopy.as_view()),
    path('apiv1/About/<device_auth>', views.LoadAbout.as_view()),
    path('apiv1/TrackDownloads/<type>/<id>/<device_auth>', views.TrackDownloads.as_view()),
    path('apiv1/FeedBack', views.FeedBack.as_view()),
    path('apiv1/GetTerms/<device_auth>', views.LoadFeedBack.as_view()),
    path('apiv1/ContactUS', views.ContactUS.as_view()),
    path('apiv1/ValidateOTP/<otp>/<device_auth>', views.ValidateOTP.as_view()),
    path('apiv1/NotesTracker/<type>/<email_uniqueid>/<device_auth>', views.NotesTracker.as_view()),
    path('apiv1/TrackerOTP/<otp>/<email>/<device_auth>', views.TrackerOTPValidater.as_view()),
    path('apiv1/Redeem/<mapped_key>/<device_auth>', monetize.RedeemAmount.as_view()),
    path('apiv1/Statement/<mapped_key>/<device_auth>', monetize.GenerateStatements.as_view()),
    #path('apiv1/ShowBills/<mapped_key>/<device_auth>', monetize.ShowBills.as_view()),
    # API ENDS HERE
    #TEMPLATE RENDERING STARTS HERE
    path('Dashboard', template_views.LoadDashBoard),
    path('PrivacyPolicy', template_views.LoadPrivacyPolicy),
    path('Terms', template_views.LoadTerms),
    path('AboutUS', template_views.LoadAboutus),
    path('UserNotesUpload/<id>/<device_auth>/<link_mapper>', template_views.UserNotesUpload),
    path('ThankYou/',template_views.ThankYou ),
    path('NotesLogin/', template_views.NotesLogin),
    path('NotesMain/', template_views.NotesMain),
    path('NoteApprove/<id>/', template_views.NotesApprove),
    path('FetchSub/', template_views.FetchSubjects),
    path('ApproveNotes/<id>', template_views.ApproveNotes),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)