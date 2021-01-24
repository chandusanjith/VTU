from .models import PaymentNotesDownloadTracker,PaymentParameter,UserMoneyBucket,MasterNotes
from django.db.models import F
from .automaticmail import SendEmail
from .OTPGenerator import GenerateOTP
from .Autherizer import AuthRequired
from rest_framework import status
from rest_framework.response import Response


def MonetizeNotes(id):
    paymentData = PaymentParameter.objects.all()
    notesData = MasterNotes.objects.filter(id=id)
    email = notesData[0].owner_email
    if UserMoneyBucket.objects.filter(email=email).exists():
        pass
    else:
        userMM = UserMoneyBucket(email=email, totAmountEarned=0, totAmountRedeemed=0)
        userMM.save()
    if PaymentNotesDownloadTracker.objects.filter(notesID=id).exists():
        trackerData = PaymentNotesDownloadTracker.objects.filter(notesID=id)
        if trackerData[0].initialViews <= paymentData[0].totEligibleViews:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(initialViews=F('initialViews') + 1)
        elif trackerData[0].initialViews > paymentData[0].totEligibleViews and trackerData[0].initialViews != 999:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(initialViews=999)
        else:
            pass

        if trackerData[0].maxViews <= paymentData[0].validViews:
            print("comig here")
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(
                maxViews=F('maxViews') + 1)
        elif trackerData[0].maxViews > paymentData[0].validViews:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(maxViews=0)
            UserMoneyBucket.objects.filter(email=email).update(
                totAmountEarned=F('totAmountEarned') + paymentData[0].eligibleViewsAmt)
            amtData = UserMoneyBucket.objects.filter(email=email)
            context = {
                'amount':paymentData[0].eligibleViewsAmt,
                'tot_earnings': amtData[0].totAmountEarned,
                'wallet': amtData[0].totAmountRedeemed,
                'min_redeem': paymentData[0].minRedeemAmt
            }
            subject = 'Hurray you just earned ' + str(paymentData[0].eligibleViewsAmt) + ' from VTU FREE NOTES.'
            SendEmail(email, context, subject, 'EarningNotify.html')
        else:
            pass
    else:
        Payments = PaymentNotesDownloadTracker(notesID = id,initialViews = 1, maxViews = 1)
        Payments.save()
        UserMoneyBucket.objects.filter(email=email).update(
            totAmountEarned=F('totAmountEarned') + paymentData[0].notesInitialAmt)
        amtData = UserMoneyBucket.objects.filter(email=email)
        context = {
            'amount': paymentData[0].notesInitialAmt,
            'tot_earnings': amtData[0].totAmountEarned,
            'wallet': amtData[0].totAmountRedeemed,
            'min_redeem': paymentData[0].minRedeemAmt
        }
        subject = 'Hurray you just earned ' + str(paymentData[0].notesInitialAmt) + ' from VTU FREE NOTES.'
        SendEmail(email, context, subject, 'EarningNotify.html')
    return True