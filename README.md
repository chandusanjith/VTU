#### Using username "ubuntu".
#### Authenticating with public key "imported-openssh-key"
#### Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-1029-aws x86_64)

#### * Documentation:  https://help.ubuntu.com
#### * Management:     https://landscape.canonical.com
#### * Support:        https://ubuntu.com/advantage

####  System information as of Wed Jan 20 19:02:45 UTC 2021

####  System load:  0.0               Processes:             113
####  Usage of /:   27.7% of 7.69GB   Users logged in:       0
####  Memory usage: 41%               IPv4 address for eth0: 172.31.26.210
####  Swap usage:   0%

#### * Introducing self-healing high availability clusters in MicroK8s.

### from now without device id my backend will not process any request.

# *******************************************************************************************
# Important note:
## Below api description is to know why and how to use the API's.
## If you want to test the API's then goto https://vtu.pythonanywhere.com/swagger/apiv1/Doc which is staging.
## From next update staging app data will be syncing with production app data.
## All the testing should be done in staging app only.
# ********************************************************************************************



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


#### https://vtu.pythonanywhere.com/apiv1/GetTerms/device_auth
### above api returns terms and conditions

#### https://vtu.pythonanywhere.com/apiv1/ContactUS
### above api used to open contact us where you need to send json data in below format.

#### {
#### "name":"cs",
#### "email":"chandusanjith.t.2610@gmail.com",
#### "contact":"6360723237",
#### "device_id":"1234567891234567",
#### "user_message":"testing"
#### }

#### https://vtu.pythonanywhere.com/apiv1/ValidateOTP/otp>/device_auth
### using this send me the otp and dev id.

#### https://vtu.pythonanywhere.com/NotesTracker/type/email_uniqueid/device_auth 
### Here send me type of user ("NEW" --> If mapped key not found, "OLD" --> If mapped key found).
### email_uniqueid --> Here if type is "NEW" send me email in this field, If type is "OLD" send me mapped_id in this field.

#### https://vtu.pythonanywhere.com/apiv1/TrackerOTP/otp/email/device_auth
### Here if you got "OTP Has been shared" in NotesTracker API then send me otp with email here