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
from vtu import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apiv1/LoadMasterData/', views.FetchMasterList.as_view()),
    path('apiv1/Notes/<sem>/<branch>/<subject>', views.SnippetList.as_view()),
    path('apiv1/Subjects/<sem>/<branch>',views.FetchSubject.as_view() ),
    path('apiv1/QP/<sem>/<branch>/<subject>', views.QuestionPaperList.as_view()),
    path('apiv1/LabVid/<sem>/<branch>/<subject>/<program_id>', views.LabManualVid.as_view()),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)