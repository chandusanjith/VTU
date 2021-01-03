
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