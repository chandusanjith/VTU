from .models import *
from django.db.models import F
from .automaticmail import SendEmail
from .OTPGenerator import GenerateOTP
from .Autherizer import AuthRequired
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from collections import namedtuple
from .serializers import *
from django.utils import timezone
from .render import Render


class RedeemAmount(APIView):
    def get(self, request, mapped_key,  device_auth, format=None):
        if AuthRequired(device_auth) == True:
            if EmailUniqueidMapper.objects.filter(mapped_id=mapped_key).exists():
                mappedData = EmailUniqueidMapper.objects.filter(mapped_id=mapped_key).first()
            else:
                return Response({"ERROR": "Type and Mapped Key not matching :("},
                                status=status.HTTP_404_NOT_FOUND)
            email = mappedData.email
            amtData = UserMoneyBucket.objects.filter(email=email).first()
            earnedAmount = amtData.totAmountEarned
            redeemedAmount = amtData.totAmountRedeemed
            UserMoneyBucket.objects.filter(email=email).update(totAmountEarned=0, totAmountRedeemed=earnedAmount+redeemedAmount)
            narration = "Self Redeemed"
            passbook = PaymentPassBook(email=email, credit=0, debit=earnedAmount,
                                       currBalance=amtData.totAmountEarned, narration=narration)
            passbook.save()
            contact_details = ContactUs.objects.filter(device_id=device_auth, email=email).first()
            context = {
                'amount': earnedAmount,
                'contact': contact_details.contact,
                'email': email,
            }
            subject = 'Redeem Alert from VTU Free Notes!'
            mail_status = SendEmail(email, context, subject, 'Redeem.html')
            if mail_status == False:
                return Response({"ERROR": "OOPS! an internal error occured :("}, status=status.HTTP_404_NOT_FOUND)
            admin_emails = AdminEmailId.objects.all()
            for reciever_mail in admin_emails:
                mail_status = SendEmail(reciever_mail.mail_reciever_email, context, subject,
                                        'Redeem.html')
                if mail_status == False:
                    return Response({"ERROR": "OOPS! an internal error occured :("},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    unique_id = mapped_key
                    if EmailUniqueidMapper.objects.filter(mapped_id=unique_id).exists():
                        mappedData = EmailUniqueidMapper.objects.filter(mapped_id=unique_id).first()
                    else:
                        return Response({"ERROR": "Type and Mapped Key not matching :("},
                                            status=status.HTTP_404_NOT_FOUND)
                    email = mappedData.email
                    TrackerRecords = namedtuple('TrackerRecords', ('NotesTrack', 'Earnings'))
                    Tracker = TrackerRecords(
                            NotesTrack=MasterNotes.objects.filter(owner_email=email),
                            Earnings=UserMoneyBucket.objects.filter(email=email),
                        )
                    if not Tracker:
                        return Response({"ERROR": "404 NO DATA FOUND :(",
                                             "Mapped_key": unique_id}, status=status.HTTP_404_NOT_FOUND)
                        # serializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth}
                        # ).data
                    notesTrackerSerializer = TrackMasterSerializer(Tracker, context={'Device_key': device_auth,
                                                                                         'Mapped_Key': unique_id,
                                                                                         'Email': email}).data
                    return Response(notesTrackerSerializer, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)


def MonetizeNotes(id):
    paymentData = PaymentParameter.objects.filter(id=1).first()
    notesData = MasterNotes.objects.filter(id=id).first()
    email = notesData.owner_email
    if UserMoneyBucket.objects.filter(email=email).exists():
        pass
    else:
        userMM = UserMoneyBucket(email=email, totAmountEarned=0, totAmountRedeemed=0)
        userMM.save()
    if PaymentNotesDownloadTracker.objects.filter(notesID=id).exists():
        trackerData = PaymentNotesDownloadTracker.objects.filter(notesID=id).first()
        if trackerData.initialViews <= paymentData.totEligibleViews:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(initialViews=F('initialViews') + 1)
        elif trackerData.initialViews > paymentData.totEligibleViews and trackerData.initialViews != 999:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(initialViews=999)
            UserMoneyBucket.objects.filter(email=email).update(
                totAmountEarned=F('totAmountEarned') + paymentData.notesInitialAmt)
            amtData = UserMoneyBucket.objects.filter(email=email).first()
            narration = "Earned for reaching " + str(paymentData.totEligibleViews) + " for notes " + notesData.Description
            passbook = PaymentPassBook(email = email, credit=paymentData.notesInitialAmt, debit=0, currBalance=amtData.totAmountEarned, narration=narration)
            passbook.save()
            context = {
                'amount': paymentData.notesInitialAmt,
                'tot_earnings': amtData.totAmountEarned,
                'wallet': amtData.totAmountRedeemed,
                'min_redeem': paymentData.minRedeemAmt,
                'eligible_views': paymentData.totEligibleViews,
                'earning_show': "1"
            }
            subject = 'Hurray you just earned ' + str(paymentData.notesInitialAmt) + ' from VTU FREE NOTES.'
            SendEmail(email, context, subject, 'EarningNotify.html')
        else:
            pass

        if trackerData.maxViews <= paymentData.validViews:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(
                maxViews=F('maxViews') + 1)
        elif trackerData.maxViews > paymentData.validViews:
            PaymentNotesDownloadTracker.objects.filter(notesID=id).update(maxViews=0)
            UserMoneyBucket.objects.filter(email=email).update(
                totAmountEarned=F('totAmountEarned') + paymentData.eligibleViewsAmt)
            amtData = UserMoneyBucket.objects.filter(email=email).first()
            narration = "Earned for reaching " + str(paymentData.validViews) + " for notes " + notesData.Description
            passbook = PaymentPassBook(email=email, credit=paymentData.eligibleViewsAmt, debit=0,
                                       currBalance=amtData.totAmountEarned, narration=narration)
            passbook.save()
            context = {
                'amount':paymentData.eligibleViewsAmt,
                'tot_earnings': amtData.totAmountEarned,
                'wallet': amtData.totAmountRedeemed,
                'min_redeem': paymentData.minRedeemAmt,
                'eligible_views':paymentData.totEligibleViews,
                'earning_show': "1"
            }
            subject = 'Hurray you just earned ' + str(paymentData.eligibleViewsAmt) + ' from VTU FREE NOTES.'
            SendEmail(email, context, subject, 'EarningNotify.html')
        else:
            pass
    else:
        Payments = PaymentNotesDownloadTracker(notesID = id,initialViews = 1, maxViews = 1)
        Payments.save()
        amtData = UserMoneyBucket.objects.filter(email=email).first()
        context = {
            'amount': paymentData.notesInitialAmt,
            'tot_earnings': amtData.totAmountEarned,
            'wallet': amtData.totAmountRedeemed,
            'min_redeem': paymentData.minRedeemAmt,
            'eligible_views': paymentData.totEligibleViews,
            'earning_show':"0",
        }
        subject = 'Hurray your notes was approved from VTU FREE NOTES.'
        SendEmail(email, context, subject, 'EarningNotify.html')
    return True


class GenerateStatements(APIView):
    def get(self, request, mapped_key,  device_auth, format=None):
        if AuthRequired(device_auth) == True:
            if EmailUniqueidMapper.objects.filter(mapped_id=mapped_key).exists():
                mappedData = EmailUniqueidMapper.objects.filter(mapped_id=mapped_key).first()
            else:
                return Response({"ERROR": "Type and Mapped Key not matching :("},
                                status=status.HTTP_404_NOT_FOUND)
            email = mappedData.email
            passbook = PaymentPassBook.objects.filter(email=email)
            today = timezone.now()
            params = {
                     'email':email,
                    'today': today,
                    'passbook': passbook,
                    'request': request
                }
            file = Render.render_to_file('Statement.html', params)
            file_path = '/media/'+file
            return Response({'statement':file_path}, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Access Denied"}, status=status.HTTP_404_NOT_FOUND)