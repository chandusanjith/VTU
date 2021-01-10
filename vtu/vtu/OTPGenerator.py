from .models import OTPValidate
from .automaticmail import SendEmail

def GenerateOTP(dev_id, email, name):
    from random import randint
    range_start = 10 ** (5 - 1)
    range_end = (10 ** 5) - 1
    otp = randint(range_start, range_end)
    if OTPValidate.objects.filter(device_id=dev_id).exists():
        OTPValidate.objects.filter(device_id=dev_id).update(otp=otp, email=email)
    else:
        ws_otp = OTPValidate(device_id=dev_id, otp=otp, email=email)
        ws_otp.save()
    context = {
        'name': name,
        'otp': otp
    }
    subject = 'Hello ' + name + ' please find the OTP'
    mail_value = SendEmail(email, context, subject, 'OTPMail.html')
    return mail_value