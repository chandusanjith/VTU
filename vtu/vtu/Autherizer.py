from .models import *
from datetime import date, timedelta
import random
import string
from rest_framework.response import Response
from rest_framework import status

def AuthRequired(auth_key):
  if len(auth_key) != 16:
    return False
  if DeviceAuth.objects.filter(device_key=auth_key).exists():
    return True
  else:
    return False

def LinkAutherizer(email):
  if EmailUniqueidMapper.objects.filter(email=email).exists():
    #data = EmailUniqueidMapper.objects.filter(email=email).first()
    link_expiry = date.today() + timedelta(days=2)
    link_mapper = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    EmailUniqueidMapper.objects.filter(email=email).update(link_mapper=link_mapper,link_expiry=link_expiry)
    return link_mapper
  else:
    return Response({"ERROR": "Error occured at LinkAutherizer"}, status=status.HTTP_404_NOT_FOUND)

def AuthLink(email,link_mapper):
  if EmailUniqueidMapper.objects.filter(link_mapper=link_mapper, email=email).exists():
    data = EmailUniqueidMapper.objects.filter(link_mapper=link_mapper, email=email).first()
    if data.link_expiry >= date.today():
      return True
    else:
      return False
  else:
    return Response({"ERROR": "Error occured at AuthLink"}, status=status.HTTP_404_NOT_FOUND)