
# VTU API
### Send get request using the url : https://vtu.pythonanywhere.com/apiv1/LoadMasterData/1234567891234567
here 1234567891234567 ---> is unique devuce id (it supports varchars)

### Response

![alt text](https://github.com/chandusanjith/VTU/blob/master/vtu1.png?raw=true)

### Now send get request using branch and semester as parameters to get subjects list:
#### https://vtu.pythonanywhere.com/apiv1/Subjects/3rd%20SEMESTER/Information%20Science%20&%20Engineering/<device_id>
### Response:
![alt text](https://github.com/chandusanjith/VTU/blob/master/vtu2.png?raw=true)

### Now send get request using branch, semester, subject-code as parameters to get notes related raw data:
#### https://vtu.pythonanywhere.com/apiv1/Notes/3rd%20SEMESTER/Information%20Science%20&%20Engineering/analog%20engineering/<device_id>

### Response:

![alt text](https://github.com/chandusanjith/VTU/blob/master/vtu3.png?raw=true)



### LabManual video featre API end API

### https://vtu.pythonanywhere.com/apiv1/LabVid/3rd%20SEMESTER/Information%20Science%20&%20Engineering/Analog%20and%20Digital%20Electronics%20Laboratory/1/<device_id>

### from now without device id my backend will not process any request.


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
""
    
###    'apiv1/InitialLoad/<device_auth>'
### Load the app initially where backend creates new device or authenticates old device
###    'apiv1/LoadMasterData/<device_auth>
### FROM HERE ALL API CALLS SHOULD BE MADE WITH DEVICE ID AS PARAMETER IF NOT KY BACKEND WILL NOT PROCESS ANY REQUEST. 
###    'apiv1/Notes/<sem>/<branch>/<subject>/<device_auth>'
### ABOVE API IS FOR NOTES
###    'apiv1/Subjects/<sem>/<branch>/<device_auth>'
### ABOVE API IS FOR SUBJECTS
###    'apiv1/QP/<sem>/<branch>/<subject>/<device_auth>'
### ABOVE API IS FOR QUESTION PAPER 
###    'apiv1/LabVid/<sem>/<branch>/<subject>/<program_id>/<device_auth>'
### ABOVE API IS FOR LAB VIDEO
###    'apiv1/LoadSyllabusCopy/<device_auth>'
### ABOVE API FOR SYLLABUS COPY
