
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


##  https://vtu.pythonanywhere.com/apiv1/InitialLoad/device_auth
### Load the app initially where backend creates new device or authenticates old device

##  https://vtu.pythonanywhere.com/apiv1/LoadMasterData/device_auth
### FROM HERE ALL API CALLS SHOULD BE MADE WITH DEVICE ID AS PARAMETER IF NOT KY BACKEND WILL NOT PROCESS ANY REQUEST.

## https://vtu.pythonanywhere.com/apiv1/Notes/sem/branch/subject/device_auth
### ABOVE API IS FOR NOTES

## https://vtu.pythonanywhere.com/apiv1/Subjects/sem/branch/device_auth
### ABOVE API IS FOR SUBJECTS

##  https://vtu.pythonanywhere.com/apiv1/QP/sem/branch/subject/device_auth
### ABOVE API IS FOR QUESTION PAPER 

##  https://vtu.pythonanywhere.com/apiv1/LabVid/'sem'/branch/subject/program_id/device_auth
### ABOVE API IS FOR LAB VIDEO

## https://vtu.pythonanywhere.com/apiv1/LoadSyllabusCopy/device_auth
### ABOVE API FOR SYLLABUS COPY

##  https://vtu.pythonanywhere.com/apiv1/TrackDownloads/type/id/device_auth
### ABOVE API CALL IS FOR TRACKING DOWNLOADS AND VIDEO VIEWS.
#### type -->  Notes -> notes
####            Qpaper -> question paper
####            SBcopy -> syllabus copy
####            LabVid -> Lab Video
#### id --> send id which i return through json response

## https://vtu.pythonanywhere.com/apiv1/FeedBack
### ABOVE API IS TO SEND FEEDBACK AND INPUT SHOULD BE IN THE FORMAT GIVEN BELOW

##### {
##### "device_id":"1234567891234567",
##### "name":"chandu sanjith",
##### "email":"chandusanjith@gmail.com",
##### "contact_number":"6360723237",
##### "feed_back":"Very nice app"
##### }