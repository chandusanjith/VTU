from .models import OTPValidate, TrackerOTPValidate
from .automaticmail import SendEmail

def GenerateOTP(dev_id, email, name,type):
    from random import randint
    range_start = 10 ** (5 - 1)
    range_end = (10 ** 5) - 1
    otp = randint(range_start, range_end)
    if type == "C":
        if OTPValidate.objects.filter(device_id=dev_id).exists():
            OTPValidate.objects.filter(device_id=dev_id).update(otp=otp, email=email)
        else:
            ws_otp = OTPValidate(device_id=dev_id, otp=otp, email=email)
            ws_otp.save()
    elif type == "N":
        if TrackerOTPValidate.objects.filter(email = email).exists():
            TrackerOTPValidate.objects.filter(email = email).update(otp=otp)
        else:
            ws_otp = TrackerOTPValidate(otp=otp, email=email)
            ws_otp.save()
    context = {
        'name': name,
        'otp': otp
    }
    subject = 'Hello ' + name + ' please find the OTP'
    mail_value = SendEmail(email, context, subject, 'OTPMail.html')
    return mail_value